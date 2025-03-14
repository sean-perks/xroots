**README: xroots Seed Collection Trend Analysis**

### Input Data Format
The program expects a CSV file with the following columns:
- `date_collected`: The date seeds were collected (format: YYYY-MM-DD)
- `species`: The species USDA plant code (ACMIO, CHAN9..))
- `amount_collected`: The lbs seeds collected (float)

Alternatively, if no CSV is provided, random seed data will be generated so the program can be tested

### Overview of Functionality
- **`SeedDataProcessor`**: Loads data from a CSV or generates synthetic data. Allows filtering by species.
- **`TrendAnalyzer`**: Fits a linear trendline to the seed collection data.
- **`Plotter`**: Visualizes the trendline over time without raw data points.

### Usage
1. Ensure the CSV file is correctly formatted (if using real data).
2. Run the script: `python main.py`
3. View the plotted trendline for different species.

