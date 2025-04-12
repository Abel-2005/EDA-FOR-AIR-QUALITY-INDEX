import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)  # or whatever you prefer
pd.set_option('display.width', None)
sns.set(style="whitegrid")


file_path = "C:/Users/abelb/Downloads/who_ambient_air_quality_database_version_2024_(v6.1).csv"
df = pd.read_csv(file_path, encoding='latin1')
df.drop(['web_link', 'reference', 'who_ms'], axis=1, inplace=True)

print(df.info())
df.nunique

print(df.describe())



numeric_cols = [
    'year', 'pm10_concentration', 'pm25_concentration', 'no2_concentration',
    'pm10_tempcov', 'pm25_tempcov', 'no2_tempcov', 'population',
    'latitude', 'longitude', 
]

non_numeric_cols = [
    'who_region', 'iso3', 'country_name', 'city', 'version',
    'type_of_stations'
]

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].mean())

for col in non_numeric_cols:
    if df[col].isna().any():
        mode_value = df[col].mode()
        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value[0])
print(df.isnull().sum())        

for col in df.select_dtypes(include='object').columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique value{'s' if unique_count > 1 else ''}")
    
print(df.columns)

country_filter = 'India'
df_country = df[df['country_name'] == country_filter]

country_trends = df_country.groupby('year')[['pm25_concentration', 'pm10_concentration', 'no2_concentration']].mean().reset_index()

country_trends.rename(columns={
    'pm25_concentration': 'PM2.5',
    'pm10_concentration': 'PM10',
    'no2_concentration': 'NO₂'
}, inplace=True)

plt.figure(figsize=(12, 6))
sns.lineplot(data=country_trends, x='year', y='PM2.5', marker='o', label='PM2.5')
sns.lineplot(data=country_trends, x='year', y='PM10', marker='o', label='PM10')
sns.lineplot(data=country_trends, x='year', y='NO₂', marker='o', label='NO₂')

plt.title(f'Pollution Trends in {country_filter}')
plt.xlabel('Year')
plt.ylabel('Average Concentration (µg/m³)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Pollutant')
plt.tight_layout()
plt.show()





year_filter = 2020
country_filter = 'India'

top_cities = df[
    (df['year'] == year_filter) & 
    (df['country_name'] == country_filter)
][['city', 'pm25_concentration']] \
.sort_values(by='pm25_concentration', ascending=False) \
.dropna().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=top_cities, x='pm25_concentration', y='city', palette='mako')
plt.title(f'Top 10 Most Polluted Cities in {country_filter} (PM2.5) - {year_filter}')
plt.xlabel('PM2.5 Concentration (µg/m³)')
plt.ylabel('City')
plt.tight_layout()
plt.show()




region_avg = df.groupby('who_region')[['pm10_concentration', 'pm25_concentration', 'no2_concentration']].mean().reset_index()
region_avg_melted = region_avg.melt(id_vars='who_region', var_name='Pollutant', value_name='Average Concentration')

plt.figure(figsize=(14, 6))
sns.barplot(data=region_avg_melted, x='who_region', y='Average Concentration', hue='Pollutant')
plt.title('Average Pollutant Concentration by WHO Region')
plt.xticks(rotation=45)
plt.show()


avg_india = df[df['country_name'] == 'India'].groupby('year')['pm25_concentration'].mean()
avg_global = df.groupby('year')['pm25_concentration'].mean()

plt.figure(figsize=(12, 6))
plt.plot(avg_india.index, avg_india.values, label='India', marker='o', linewidth=2)
plt.plot(avg_global.index, avg_global.values, label='Global Average', marker='o', linewidth=2)
plt.title('PM2.5 Trends Over Years: India vs Global')
plt.xlabel('Year')
plt.ylabel('PM2.5 (µg/m³)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()




city_name = 'Delhi/IND'
year_filter = 2020

city_data = df[(df['country_name'] == 'India') & (df['city'].str.lower() == city_name.lower()) & (df['year'] == year_filter)]

if not city_data.empty:
    values = city_data[['pm25_concentration', 'pm10_concentration', 'no2_concentration']].iloc[0]
    labels = ['PM2.5', 'PM10', 'NO2']
    
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['crimson', 'orange', 'purple'])
    plt.title(f'Pollution Composition in {city_name.title()} - {year_filter}')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
else:
    print(f"No data available for {city_name} in {year_filter}")

pivot_df = df.pivot_table(
    index='country_name', 
    values=['pm25_concentration', 'pm10_concentration', 'no2_concentration'], 
    aggfunc='mean'
).dropna().sort_values(by='pm25_concentration', ascending=False).head(20)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_df, annot=True, cmap='YlOrRd', fmt=".1f")
plt.title('Pollutant Concentration by Country (Top 20)')
plt.xlabel('Pollutant')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title('Correlation Matrix of Numeric Features')
plt.tight_layout()
plt.show()








