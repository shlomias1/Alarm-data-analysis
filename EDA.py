import pandas as pd
from process import alarms, coords
 
# ======= EDA ==========================================
def get_general_summary(df):
    print("General summary of the dataset:")
    summary = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum(),
        'info': df.info(),
        'head': df.head()
    }
    print(summary)
    return summary

def EDA_numerical_summary(df):
    numerical_summary = df.describe(include='number')
    print("EDA numerical summary")
    print(numerical_summary)
    return numerical_summary

def check_nulls(df):
    nulls = df.isnull().sum().to_frame(name='null_count')
    nulls['percentage'] = (nulls['null_count'] / len(df) * 100).round(2)
    print("Nulls in the dataset:")
    print(nulls)
    return nulls

def show_nulls(df):
    missing_info = df[
        alarms['region'].isnull() | df['alarm_time'].isnull() | df['km_from_Gaza'].isnull()
    ]

    missing_info_summary = missing_info[['cities', 'km_from_Gaza', 'region', 'region_en', 'alarm_time']].drop_duplicates()
    print("Missing information summary:")
    print(missing_info_summary)
    return missing_info_summary

def drill_down_nulls(alarms,coords):
    # Find cities with missing region info
    missing_region = alarms[alarms['region'].isnull()]['cities'].unique()
    # Check if these cities exist in the coords file (before merge)
    cities_in_coords = coords['loc'].unique()
    missing_in_coords = [city for city in missing_region if city not in cities_in_coords]
    # Create a DataFrame to display
    missing_check = pd.DataFrame({
        'city_missing_region': missing_region,
        'exists_in_coords': [city in cities_in_coords for city in missing_region]
    })
    print("Cities with missing region info and their existence in coords:")
    print(missing_check)
    return missing_check

def Description_distribution(df):
    desc_distribution = df['description_en'].value_counts().to_frame(name='count')
    desc_distribution['percentage'] = (desc_distribution['count'] / len(df) * 100).round(2)
    print("Description distribution:")
    print(desc_distribution)
    return desc_distribution

def Region_desc_distribution(df):
    region_distribution = df['region_en'].value_counts().to_frame(name='count')
    region_distribution['percentage'] = (region_distribution['count'] / len(df) * 100).round(2)
    print("region distribution")
    print(region_distribution)
    return region_distribution

def plot(df):
    df['region_en'].value_counts().plot(kind='barh')
    print(df.groupby('region_en')['alarm_time_filled'].mean().sort_values())
    df['threat'].value_counts().sort_index().plot(kind='bar')
    df.groupby('month-year').size().plot()

def EDA():
    get_general_summary(alarms)
    EDA_numerical_summary(alarms)
    check_nulls(alarms)
    show_nulls(alarms)
    drill_down_nulls(alarms,coords)
    Description_distribution(alarms)
    Region_desc_distribution(alarms)
    plot(alarms)

if __name__ == "__main__":
    EDA()