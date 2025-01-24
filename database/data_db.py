import logging
from typing import List, Dict, Any, Optional
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)


class DataDB:
    def __init__(self, db_connection):
        self.db = db_connection

    def add_patient(self, data: Dict[str, Any], user_id: int) -> bool:
        try:
            # Create anonymized ID
            data_str = f"{data['medical_unit']}{data['age']}{data['sex']}{datetime.now()}"
            anonymized_id = hashlib.sha256(data_str.encode()).hexdigest()

            columns = list(data.keys()) + ['anonymized_id', 'uploaded_by']
            placeholders = ', '.join(['%s'] * len(columns))

            query = f"""
                INSERT INTO Patients ({', '.join(columns)})
                VALUES ({placeholders})
            """

            values = list(data.values()) + [anonymized_id, user_id]
            success = self.db.execute_query(query, values)

            return success
        except Exception as e:
            logger.error(f"Error adding patient data: {e}")
            return False

    def get_patients(self, filters: Optional[Dict[str, Any]] = None,
                     limit: int = 1000) -> List[Dict[str, Any]]:
        try:
            query = "SELECT * FROM Patients WHERE 1=1"
            params = []

            if filters:
                for key, value in filters.items():
                    query += f" AND {key} = %s"
                    params.append(value)

            query += f" LIMIT {limit}"

            self.db.execute_query(query, params if params else None)
            return self.db.fetchall()
        except Exception as e:
            logger.error(f"Error fetching patient data: {e}")
            return []

    def update_patient(self, patient_id: int, data: Dict[str, Any],
                       user_id: int) -> bool:
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"""
                UPDATE Patients 
                SET {set_clause}
                WHERE patient_id = %s
            """

            values = list(data.values()) + [patient_id]
            success = self.db.execute_query(query, values)

            return success
        except Exception as e:
            logger.error(f"Error updating patient data: {e}")
            return False

    def delete_patient(self, patient_id: int, user_id: int) -> bool:
        try:
            query = "DELETE FROM Patients WHERE patient_id = %s"
            success = self.db.execute_query(query, (patient_id,))

            return success
        except Exception as e:
            logger.error(f"Error deleting patient data: {e}")
            return False
