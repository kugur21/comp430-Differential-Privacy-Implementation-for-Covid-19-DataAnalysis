# Import preprocessing libraries
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Preprocessing function
def preprocess_data(input_file, output_file):
    # Load the dataset
    covid_data = pd.read_csv(input_file)

    # Replace placeholder values with NaN
    placeholder_values = [97, 99]
    covid_data.replace(placeholder_values, np.nan, inplace=True)

    # Separate numeric and non-numeric columns
    numeric_columns = covid_data.select_dtypes(include=['float64', 'int64']).columns
    non_numeric_columns = covid_data.select_dtypes(exclude=['float64', 'int64']).columns

    # Apply KNN Imputation to numeric columns only
    imputer = KNNImputer(n_neighbors=5)
    covid_data[numeric_columns] = imputer.fit_transform(covid_data[numeric_columns])

    # Process non-numeric columns
    if 'DATE_DIED' in non_numeric_columns:
        covid_data['DATE_DIED'] = pd.to_datetime(covid_data['DATE_DIED'], errors='coerce')
        covid_data['DATE_DIED'] = covid_data['DATE_DIED'].fillna(pd.Timestamp('2099-12-31'))
        covid_data['SURVIVED'] = (covid_data['DATE_DIED'] == pd.Timestamp('2099-12-31')).astype(int)

    # Encode categorical variables
    categorical_columns = ['SEX', 'CLASIFFICATION_FINAL']
    for column in categorical_columns:
        encoder = LabelEncoder()
        covid_data[column] = encoder.fit_transform(covid_data[column].astype(str))

    # Scale numeric columns
    scaler = StandardScaler()
    scaled_columns = ['AGE', 'MEDICAL_UNIT', 'ICU']
    covid_data[scaled_columns] = scaler.fit_transform(covid_data[scaled_columns])

    # Save the cleaned data to a new CSV file
    covid_data.to_csv(output_file, index=False)

