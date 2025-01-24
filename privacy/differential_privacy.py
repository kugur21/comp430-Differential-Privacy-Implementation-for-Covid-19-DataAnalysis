import numpy as np


def apply_differential_privacy(data, mechanism="Gaussian", epsilon=2.0, utility=None, sensitivity=1):
    """
    Verilen 'data' (sayı listesi) için istenen mekanizma doğrultusunda
    diferansiyel gizlilik (DP) uygular.

    Parametreler:
    -------------
    data : list of float
        Sayısal değerlerin listesi (örneğin sorgu sonuçları).
    mechanism : str
        Kullanılacak mekanizma adı ("Gaussian", "Laplace", "ReportNoisyMax", "Exponential").
    epsilon : float
        Gizlilik bütçesi (privacy budget).
    utility : list of float, optional
        Exponential mekanizması için fayda (utility) değerleri.
    sensitivity : float, optional
        Sorgunun duyarlılığı (ör. sayımlar için 1).
    """
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


def gaussian_mechanism(data, epsilon, delta, sensitivity=1):
    sigma = np.sqrt(2 * np.log(1.25 / delta)) * sensitivity / epsilon
    noise = np.random.normal(0, sigma, len(data))
    return [x + n for x, n in zip(data, noise)]


def laplace_mechanism(data, epsilon, sensitivity=1):
    """
    Laplace gürültüsü ekleyen mekanizma.

    Eğer bir sayım sorgusu yapıyorsak, sensitivity = 1 alınması tipiktir.
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, len(data))
    return [x + n for x, n in zip(data, noise)]


def report_noisy_max(data, epsilon, sensitivity=1):
    """
    Report Noisy Max mekanizması:
    Laplace gürültüsü ile skorları bozup en yükseği seçer.
    """
    noise = np.random.laplace(0, sensitivity / epsilon, len(data))
    noisy_scores = [x + n for x, n in zip(data, noise)]
    return noisy_scores.index(max(noisy_scores))


def exponential_mechanism(data, utility, epsilon, sensitivity=1):
    """
    Exponential mekanizması, fayda (utility) skorlarına göre
    bir elemana ihtimalen rastgele seçim yapar.
    """
    if len(data) != len(utility):
        raise ValueError("data ve utility aynı uzunlukta olmalıdır.")

    # utility değerlerini sensitivity ile ölçeklendir
    scaled_utilities = [u / sensitivity for u in utility]
    probabilities = np.exp((epsilon * np.array(scaled_utilities)) / 2)
    probabilities /= probabilities.sum()  # Normalize
    return np.random.choice(data, p=probabilities)
