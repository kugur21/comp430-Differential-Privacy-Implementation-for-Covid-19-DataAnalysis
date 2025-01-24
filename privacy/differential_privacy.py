import numpy as np

def calculate_sensitivity(db_connection, query):
    query = query.lower().strip()

    if "count" in query:
        return 1
    elif "sum" in query:
        column = query.split("sum(")[1].split(")")[0]
        max_query = f"SELECT MAX({column}) FROM Patients;"
        db_connection.execute_query(max_query)
        result = db_connection.cursor.fetchone()
        return result[f"MAX({column})"] if result else 1
    elif "avg" in query:
        column = query.split("avg(")[1].split(")")[0]
        max_query = f"SELECT MAX({column}) FROM Patients;"
        db_connection.execute_query(max_query)
        result = db_connection.cursor.fetchone()
        return result[f"MAX({column})"] if result else 1
    elif "group by" in query:
        return 1
    elif "min" in query or "max" in query:
        column = query.split("min(")[1].split(")")[0] if "min" in query else query.split("max(")[1].split(")")[0]
        max_query = f"SELECT MAX({column}) FROM Patients;"
        db_connection.execute_query(max_query)
        result = db_connection.cursor.fetchone()
        return result[f"MAX({column})"] if result else 1
    elif "case" in query:
        return 1
    elif "where" in query:
        return 1
    else:
        return 1

def apply_differential_privacy(db_connection, data, mechanism="Gaussian", epsilon=2.0, utility=None, sensitivity=None, query=None):
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
            raise ValueError("Utility is required for Exponential mechanism.")
        return exponential_mechanism(data, utility, epsilon, sensitivity)
    else:
        raise ValueError(f"Invalid Mechanism: {mechanism}")

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
        raise ValueError("Data and Utility must have the same length.")

    scaled_utilities = [u / sensitivity for u in utility]
    probabilities = np.exp((epsilon * np.array(scaled_utilities)) / 2)
    probabilities /= probabilities.sum()  # Normalize
    return np.random.choice(data, p=probabilities)