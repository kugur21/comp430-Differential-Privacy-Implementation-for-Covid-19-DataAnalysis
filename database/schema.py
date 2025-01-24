CREATE_TABLES_QUERIES = {
    'users': """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('admin', 'viewer') NOT NULL,
            budget INT DEFAULT 100,
            INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,

    'patients': """
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            usmer INT,
            medical_unit INT,
            sex INT,
            patient_type INT,
            date_died DATE,
            intubed INT,
            pneumonia INT,
            age INT,
            pregnant INT,
            diabetes INT,
            copd INT,
            asthma INT,
            inmsupr INT,
            hipertension INT,
            other_disease INT,
            cardiovascular INT,
            obesity INT,
            renal_chronic INT,
            tobacco INT,
            classification_final INT,
            icu INT,
            anonymized_id VARCHAR(64),
            uploaded_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_medical_unit (medical_unit),
            INDEX idx_date_died (date_died),
            INDEX idx_anonymized_id (anonymized_id),
            FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
}