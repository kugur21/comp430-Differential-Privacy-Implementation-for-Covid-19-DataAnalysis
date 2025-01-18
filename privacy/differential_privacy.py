import numpy as np

def apply_differential_privacy(data, mechanism="Gaussian", epsilon=1.0):
    """
    Applies a differential privacy mechanism to the data.

    :param data: A list of numerical data.
    :param mechanism: The DP mechanism to apply ("Gaussian" or "Laplace").
    :param epsilon: The privacy budget parameter.
    :return: The privacy-preserved data.
    """
    if mechanism == "Gaussian":
        return gaussian_mechanism(data, epsilon)
    elif mechanism == "Laplace":
        return laplace_mechanism(data, epsilon)
    else:
        raise ValueError(f"Unsupported mechanism: {mechanism}")

def gaussian_mechanism(data, epsilon):
    """
    Applies Gaussian noise to the data.

    :param data: A list of numerical data.
    :param epsilon: The privacy budget parameter.
    :return: The data with Gaussian noise added.
    """
    sensitivity = max(data) - min(data)  # Sensitivity is the range of the data
    sigma = sensitivity / epsilon
    noise = np.random.normal(0, sigma, len(data))
    return [x + n for x, n in zip(data, noise)]

def laplace_mechanism(data, epsilon):
    """
    Applies Laplace noise to the data.

    :param data: A list of numerical data.
    :param epsilon: The privacy budget parameter.
    :return: The data with Laplace noise added.
    """
    sensitivity = max(data) - min(data)  # Sensitivity is the range of the data
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, len(data))
    return [x + n for x, n in zip(data, noise)]
