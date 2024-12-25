import os
import pandas as pd

def extract_city_data(directory):
    
    all_data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                city_data = pd.read_csv(file_path)
                city_data['CITY'] = os.path.splitext(file)[0]  # Add a column for the city name
                all_data.append(city_data)
    
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data