import pandas as pd
import numpy as np
from diffprivlib.mechanisms import Laplace, Exponential

# Define the file path
file_path = 'reducedCovidData.csv'

# Load the CSV file
data = pd.read_csv(file_path)

# Print the first 5 rows of the data
print("Original Data:")
print(data.head())

print("Columns in the dataset:")
print(data.columns)


# Add Gaussian Noise to numerical columns
def apply_gaussian_noise(column, epsilon=1.0):
    """
    Applies Gaussian noise to a numerical column for differential privacy.

    Parameters:
    column (pd.Series): The numerical column to add noise to.
    epsilon (float): The privacy budget.

    Returns:
    pd.Series: Column with Gaussian noise added.
    """
    scale = 1 / epsilon
    noise = np.random.normal(0, scale, size=column.shape)
    return column + noise

# Example: Adding noise to the "age" column (replace 'age' with your actual numerical column name)
if 'AGE' in data.columns:
    data['AGE_noisy'] = apply_gaussian_noise(data['AGE'], epsilon=0.5)
    print("\nNoisy 'AGE' Column:")
    print(data[['AGE', 'AGE_noisy']].head())

# Apply Report Noisy Max to categorical data
def report_noisy_max(data, column, epsilon=1.0):
    """
    Implements the Report Noisy Max mechanism to identify the most frequent category privately.

    Parameters:
    data (pd.DataFrame): The dataset containing the categorical column.
    column (str): The name of the categorical column.
    epsilon (float): The privacy budget.

    Returns:
    str: The most frequent category with noisy counts.
    """
    value_counts = data[column].value_counts()
    categories, counts = value_counts.index, value_counts.values
    noisy_counts = [count + np.random.laplace(0, 1 / epsilon) for count in counts]
    return categories[np.argmax(noisy_counts)]

# Example: Finding the most frequent category in the "gender" column (replace 'gender' with your column)
if 'SEX' in data.columns:  # 'SEX' sütunu cinsiyet bilgisi içeriyor
    noisy_max_category = report_noisy_max(data, 'SEX', epsilon=1.0)
    print(f"\nMost Frequent Gender (Noisy): {noisy_max_category}")

# Apply Exponential Mechanism for selecting based on utility scores
def exponential_mechanism(utility_scores, epsilon=1.0):
    """
    Implements the Exponential Mechanism for selecting an item based on utility scores.

    Parameters:
    utility_scores (list of tuples): A list of items and their respective utility scores.
    epsilon (float): The privacy budget.

    Returns:
    str: The selected item.
    """
    items, scores = zip(*utility_scores)
    probabilities = np.exp(np.array(scores) * epsilon / 2)
    probabilities /= probabilities.sum()
    return np.random.choice(items, p=probabilities)

# Example: Applying exponential mechanism to predict ICU admission
if 'ICU' in data.columns:  # 'ICU' yoğun bakım bilgisi içeriyor
    # Örnek utility scores: Yoğun bakıma alınma durumu için fayda skorları
    utility_data = [("Admitted", 0.9), ("Not Admitted", 0.7)]
    selected_icu_admission = exponential_mechanism(utility_data, epsilon=1.0)
    print(f"\nICU Admission Prediction (DP Compliant): {selected_icu_admission}")
