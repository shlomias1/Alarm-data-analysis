import pandas as pd
from load_data import alarms, coords, time_to_impact

#time processing
alarms['time'] = pd.to_datetime(alarms['time'])
alarms['month-year'] = alarms['time'].dt.to_period('M')
alarms['year'] = alarms['time'].dt.to_period('Y')

translation_map = {
    "ירי רקטות וטילים": "Rockets",
    "חדירת כלי טיס עוין": "Hostile Aircraft",
    "רעידת אדמה": "Earthquake",
    "חדירת מחבלים": "Terrorist Infiltration",
    "אזהרה": "Warning"
}
alarms['description_en'] = alarms['description'].map(translation_map)

def categorize_region(lat, lon):
    if lat < 31.5 and lon < 35.0:
        return 'עוטף עזה'
    elif lat < 31.5 and lon >= 35.0:
        return 'דרום'
    elif 31.5 <= lat < 32.0 and lon < 35.0:
        return 'שפלה'
    elif 31.7 <= lat < 32.0 and 35.0 <= lon < 35.3:
        return 'ירושלים'
    elif 31.5 <= lat < 32.0 and lon >= 35.0:
        return 'מרכז'
    elif 32.0 <= lat < 32.5 and lon > 35.0:
        return 'שומרון'
    elif lat >= 32.5:
        return 'צפון'
    else:
        return 'אחר'

region_translation = {
    'עוטף עזה': 'Gaza Envelope',
    'דרום': 'South',
    'שפלה': 'Shfela',
    'מרכז': 'Center',
    'ירושלים': 'Jerusalem',
    'שומרון': 'Samaria',
    'צפון': 'North',
    'אחר': 'Other'
}

# Apply the function to the DataFrame
coords['region'] = coords.apply(lambda row: categorize_region(row['lat'], row['long']), axis=1)
coords['region_en'] = coords['region'].map(region_translation)

alarms = alarms.merge(
    coords[['loc','km_from_Gaza', 'region', 'region_en']], 
    left_on='cities', 
    right_on='loc',
    how='left'
)

alarms.drop(columns='loc', inplace=True)

time_to_impact["cities_temp"] = time_to_impact["cities"]
alarms = alarms.merge(
    time_to_impact[['cities_temp', 'alarm_time']], 
    left_on='cities', 
    right_on='cities_temp',
    how='left'
)

alarms.drop(columns='cities_temp', inplace=True)

# Fill missing values in 'origin' with "Unknown"
alarms['origin'] = alarms['origin'].fillna("Unknown")
alarms['origin'] = alarms['origin'].replace("Israel", "Lebanon")
# Fill missing region and region_en with 'אחר' and 'Other'
alarms['region'] = alarms['region'].fillna('אחר')
alarms['region_en'] = alarms['region_en'].fillna('Other')
# Fill missing km_from_Gaza values with 0
alarms['km_from_Gaza'] = alarms['km_from_Gaza'].fillna(0)

# Fill missing alarm_time values based on known times from the same city or region
# First, we will group by 'cities' to find known alarm times
known_alarm_times = alarms.groupby('cities')['alarm_time'].first()
# Convert 'alarm_time' to datetime for consistency
alarms['alarm_time_filled'] = alarms.apply(
    lambda row: known_alarm_times[row['cities']] if pd.isnull(row['alarm_time']) and row['cities'] in known_alarm_times else row['alarm_time'],
    axis=1
)
# If there are still missing values, we will fill them based on the average alarm time for the region
# This is a second step to ensure that any remaining NaN values are filled
region_median = alarms.groupby('region_en')['alarm_time'].median()
alarms['alarm_time_filled'] = alarms.apply(
    lambda row: region_median[row['region_en']] if pd.isnull(row['alarm_time_filled']) and row['region_en'] in region_median else row['alarm_time_filled'],
    axis=1
)

output_path = r"data/processed_alarms.xlsx"
alarms.to_excel(output_path, index=False)