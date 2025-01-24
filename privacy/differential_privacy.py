import numpy as np

def calculate_sensitivity(db_connection, query):
    """
    Sorgunun türüne göre sensitivity değerini otomatik olarak hesaplar.
    """
    query = query.lower().strip()

    if "count" in query:
        # COUNT sorguları için sensitivity genellikle 1'dir.
        return 1
    elif "sum" in query:
        # SUM sorguları için sensitivity, sütundaki maksimum değere bağlıdır.
        # Örneğin, SUM(age) için MAX(age) değerini buluruz.
        column = query.split("sum(")[1].split(")")[0]  # SUM(age) -> age
        max_query = f"SELECT MAX({column}) FROM Patients;"
        db_connection.execute_query(max_query)
        result = db_connection.cursor.fetchone()
        return result[f"MAX({column})"] if result else 1
    elif "avg" in query:
        # AVG sorguları için sensitivity, SUM ve COUNT sensitivity'lerine bağlıdır.
        # Örneğin, AVG(age) için MAX(age) / 1.
        column = query.split("avg(")[1].split(")")[0]  # AVG(age) -> age
        max_query = f"SELECT MAX({column}) FROM Patients;"
        db_connection.execute_query(max_query)
        result = db_connection.cursor.fetchone()
        return result[f"MAX({column})"] if result else 1
    elif "group by" in query:
        # GROUP BY sorguları için sensitivity genellikle 1'dir.
        return 1
    elif "min" in query or "max" in query:
        # MIN veya MAX sorguları için sensitivity, sütundaki maksimum değere bağlıdır.
        column = query.split("min(")[1].split(")")[0] if "min" in query else query.split("max(")[1].split(")")[0]
        max_query = f"SELECT MAX({column}) FROM Patients;"
        db_connection.execute_query(max_query)
        result = db_connection.cursor.fetchone()
        return result[f"MAX({column})"] if result else 1
    elif "case" in query:
        # CASE WHEN sorguları için sensitivity genellikle 1'dir.
        return 1
    elif "where" in query:
        # WHERE koşulu içeren sorgular için sensitivity genellikle 1'dir.
        return 1
    else:
        # Diğer sorgular için varsayılan sensitivity değeri.
        return 1

def apply_differential_privacy(db_connection, data, mechanism="Gaussian", epsilon=2.0, utility=None, sensitivity=None, query=None):
    """
    Diferansiyel gizlilik mekanizmalarını uygular.
    Sensitivity otomatik olarak hesaplanır veya manuel olarak belirtilir.
    """
    if sensitivity is None and query is not None:
        sensitivity = calculate_sensitivity(db_connection, query)

    if mechanism == "Gaussian":
        return gaussian_mechanism(data, epsilon, sensitivity)
    elif mechanism == "Laplace":
        return laplace_mechanism(data, epsilon, sensitivity)
    elif mechanism == "ReportNoisyMax":
        return report_noisy_max(data, epsilon, sensitivity)
    elif mechanism == "Exponential":
        if utility is None:
            raise ValueError("Exponential mekanizması için 'utility' parametresi gereklidir.")
        return exponential_mechanism(data, utility, epsilon, sensitivity)
    else:
        raise ValueError(f"Geçersiz mekanizma: {mechanism}")

def gaussian_mechanism(data, epsilon, sensitivity=1):
    sigma = np.sqrt(2 * np.log(1.25 / 1e-5)) * sensitivity / epsilon
    noise = np.random.normal(0, sigma, len(data))
    return [x + n for x, n in zip(data, noise)]

def laplace_mechanism(data, epsilon, sensitivity=1):
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, len(data))
    return [x + n for x, n in zip(data, noise)]

def report_noisy_max(data, epsilon, sensitivity=1):
    noise = np.random.laplace(0, sensitivity / epsilon, len(data))
    noisy_scores = [x + n for x, n in zip(data, noise)]
    return noisy_scores.index(max(noisy_scores))

def exponential_mechanism(data, utility, epsilon, sensitivity=1):
    if len(data) != len(utility):
        raise ValueError("data ve utility aynı uzunlukta olmalıdır.")

    scaled_utilities = [u / sensitivity for u in utility]
    probabilities = np.exp((epsilon * np.array(scaled_utilities)) / 2)
    probabilities /= probabilities.sum()  # Normalize
    return np.random.choice(data, p=probabilities)

