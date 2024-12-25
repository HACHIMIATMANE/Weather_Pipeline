import pandas as pd

def transform_data(df):
    # Drop rows with missing values
    df = df.dropna()

    # Zero-pad 'DOY' to ensure it has three digits
    df['DOY'] = df['DOY'].apply(lambda x: f"{x:03}")

    # Convert 'YEAR' and 'DOY' to datetime and set as index
    df['DATE'] = pd.to_datetime(df['YEAR'].astype(str) + df['DOY'], format='%Y%j')
    df.set_index('DATE', inplace=True)

    # Group by city and resample to monthly data
    city_groups = df.groupby('CITY')
    anomalies_list = []

    for city, group in city_groups:
        df_monthly = group.resample('M').agg({
            'PRECTOTCORR': 'sum',
            'T2M_MAX': 'mean',
            'T2M_MIN': 'mean',
            'T2M': 'mean'
        })

        # Calculate anomalies relative to a reference period (e.g., 2010-2020)
        reference_period = df_monthly[(df_monthly.index.year >= 2010) & (df_monthly.index.year <= 2020)]
        reference_means = reference_period.groupby(reference_period.index.month).mean()

        anomalies = df_monthly.copy()
        anomalies['CITY'] = city

        for month in range(1, 13):
            anomalies.loc[anomalies.index.month == month, 'PRECIPITATION_ANOMALY'] = (
                anomalies.loc[anomalies.index.month == month, 'PRECTOTCORR'] - reference_means.loc[month, 'PRECTOTCORR']
            )
            anomalies.loc[anomalies.index.month == month, 'TEMPERATURE_MAX_ANOMALY'] = (
                anomalies.loc[anomalies.index.month == month, 'T2M_MAX'] - reference_means.loc[month, 'T2M_MAX']
            )
            anomalies.loc[anomalies.index.month == month, 'TEMPERATURE_MIN_ANOMALY'] = (
                anomalies.loc[anomalies.index.month == month, 'T2M_MIN'] - reference_means.loc[month, 'T2M_MIN']
            )
            anomalies.loc[anomalies.index.month == month, 'T2M_ANOMALY'] = (
                anomalies.loc[anomalies.index.month == month, 'T2M'] - reference_means.loc[month, 'T2M']
            )

        # Normalize the data
        normalized_df = (anomalies[['PRECTOTCORR', 'T2M_MAX', 'T2M_MIN', 'T2M']] - anomalies[['PRECTOTCORR', 'T2M_MAX', 'T2M_MIN', 'T2M']].mean()) / anomalies[['PRECTOTCORR', 'T2M_MAX', 'T2M_MIN', 'T2M']].std()
        anomalies[['PRECIPITATION_NORM', 'TEMPERATURE_MAX_NORM', 'TEMPERATURE_MIN_NORM', 'TEMPERATURE_NORM']] = normalized_df

        # Add seasonal columns
        anomalies['SEASON'] = anomalies.index.month % 12 // 3 + 1
        anomalies['SEASON'] = anomalies['SEASON'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'})

        anomalies_list.append(anomalies)

    # Concatenate all city data
    all_anomalies = pd.concat(anomalies_list)

    #rename columns
    all_anomalies.rename(columns={'PRECTOTCORR': 'PRECIPITATION', 'T2M_MAX': 'MAX_TEMPERATURE', 'T2M_MIN': 'MIN_TEMPERATURE', 'T2M': 'TEMPERATURE'}, inplace=True)

    # Reorder columns

    all_anomalies = all_anomalies[['CITY', 'SEASON', 'PRECIPITATION', 'PRECIPITATION_ANOMALY', 'PRECIPITATION_NORM', 'MAX_TEMPERATURE', 'TEMPERATURE_MAX_ANOMALY', 'TEMPERATURE_MAX_NORM', 'MIN_TEMPERATURE', 'TEMPERATURE_MIN_ANOMALY', 'TEMPERATURE_MIN_NORM', 'TEMPERATURE', 'T2M_ANOMALY', 'TEMPERATURE_NORM']]

    return all_anomalies