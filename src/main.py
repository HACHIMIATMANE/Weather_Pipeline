from pipeline.extract import extract_city_data
from pipeline.transform import transform_data
from pipeline.load import load_data

def main():
    # Extract
    data = extract_city_data(r'C:\Users\darck\OneDrive\Desktop\ALL\ProjectData\WheatherPupeline\src\data')
    
    # Transform
    transformed_data = transform_data(data)
    
    # Load
    load_data(transformed_data, 'data.db')  # Pour SQLite
    # load_data(transformed_data, 'output/loaded_data.csv')  # Pour CSV
    

if __name__ == "__main__":
    main()