import numpy as np


def apply_differential_privacy(data, mechanism="Gaussian", epsilon=2.0, utility=None, sensitivity=1):

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
