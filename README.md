# Alarm Data Analysis

This project analyzes and visualizes emergency alarm data in Israel, with the goal of uncovering spatial and temporal patterns related to rocket/missile alerts and other threats. The project handles raw alarm data, enriches it with geolocation and regional metadata, and produces a cleaned dataset ready for exploratory data analysis (EDA).

---

## Project Structure

```

├── data/
│   ├── alarms.csv             # Raw alarm event data
│   ├── coords.csv             # Location coordinates and metadata
│   ├── time_to_impact.csv     # Estimated time-to-impact per city
│   └── processed_alarms.xlsx  # Output: cleaned dataset with enriched fields
├── load_data.py               # Loads raw datasets into memory
├── process.py                 # Cleans and enriches the data
├── EDA.py                     # Exploratory Data Analysis: statistics and plots

````

---

## Features

- **Data Cleaning**: Fills missing values using contextual logic (city-based and region-based interpolation).
- **Geospatial Tagging**: Assigns regions based on latitude and longitude.
- **Translation**: Converts Hebrew alarm descriptions and region names into English.
- **EDA**: Offers summary statistics, missing data reports, and distribution visualizations.

---

## Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/shlomias1/Alarm-data-analysis.git
   cd Alarm-data-analysis

2. **Install dependencies**:

   ```bash
   pip install pandas openpyxl
   ```

3. **Place CSV files** in the `data/` folder:

   * `alarms.csv`
   * `coords.csv`
   * `time_to_impact.csv`

4. **Run the processing script**:

   ```bash
   python process.py
   ```

5. **Run EDA**:

   ```bash
   python EDA.py
   ```
---

## EDA Insights

The `EDA.py` script performs the following analyses:

* Dataset dimensions, memory usage, and column data types
* Null/missing value analysis (including drill-down into city-level gaps)
* Distribution of threat types and regions
* Temporal trends (monthly analysis)
* Visualizations for alarm frequency by region and threat type

---

## Region Mapping Logic

Regions are determined based on geographic coordinates using a custom logic defined in `process.py`. Examples:

| Latitude  | Longitude | Region   |
| --------- | --------- | -------- |
| < 31.5    | < 35.0    | עוטף עזה |
| 32.0–32.5 | > 35.0    | שומרון   |
| ≥ 32.5    | any       | צפון     |

---

## Output

* `data/processed_alarms.xlsx`: Final enriched and cleaned dataset
* Terminal output: summaries, null breakdowns, and visualizations

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to improve or add.

---

## License

This project is open-source and available under the MIT License.

---

## Author

Shlomi Assayag
GitHub: [shlomias1](https://github.com/shlomias1)

```
