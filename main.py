# Read the uploaded CSV file and print the first 5 rows
import pandas as pd

# Define the file path
file_path = 'reducedCovidData.csv'

# Load the CSV file
data = pd.read_csv(file_path)

# Print the first 5 rows of the data
print(data.head())
