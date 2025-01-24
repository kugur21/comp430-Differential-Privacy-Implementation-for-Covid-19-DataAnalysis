import bcrypt

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    :param password: The plain-text password to hash.
    :return: The hashed password as a string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    :param password: The plain-text password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
