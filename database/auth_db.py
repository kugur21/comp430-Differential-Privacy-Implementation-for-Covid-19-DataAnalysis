import bcrypt
import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class AuthDB:
    def __init__(self, db_connection):
        self.db = db_connection

    def create_user(self, username: str, password: str, role: str = 'viewer') -> bool:
        try:
            # Hash password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

            query = """
                INSERT INTO Users (username, password_hash, role)
                VALUES (%s, %s, %s)
            """
            return self.db.execute_query(query, (username, password_hash.decode('utf-8'), role))
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False

    def verify_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT user_id, username, password_hash, role
                FROM Users
                WHERE username = %s
            """
            self.db.execute_query(query, (username,))
            user = self.db.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user['password_hash'].encode('utf-8')):
                # Update last login
                self._update_last_login(user['user_id'])
                return {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'role': user['role']
                }
            return None
        except Exception as e:
            logger.error(f"Error verifying user: {e}")
            return None

    def _update_last_login(self, user_id: int) -> None:
        query = """
            UPDATE Users 
            SET last_login = %s 
            WHERE user_id = %s
        """
        self.db.execute_query(query, (datetime.now(), user_id))

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        try:
            # Verify old password
            query = "SELECT password_hash FROM Users WHERE user_id = %s"
            self.db.execute_query(query, (user_id,))
            result = self.db.fetchone()

            if not result or not bcrypt.checkpw(old_password.encode('utf-8'),
                                                result['password_hash'].encode('utf-8')):
                return False

            # Update with new password
            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            update_query = """
                UPDATE Users 
                SET password_hash = %s 
                WHERE user_id = %s
            """
            return self.db.execute_query(update_query, (new_hash.decode('utf-8'), user_id))
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return False
