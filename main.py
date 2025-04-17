import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

class SeedDataProcessor:
    def __init__(self, csv_path=None, date_col=None):
        self.csv_path = csv_path
        self.date_col = date_col

    def load_data(self, species=None):
        """Loads seed collection data from a CSV or generates fake data if no CSV is provided. Filters by species if specified."""
        if self.csv_path:
            if not self.date_col:
                data = pd.read_csv(self.csv_path)
                found = False
                for c in data.columns:
                    if "date" in c.lower():
                        date_col = c
                        data[date_col] = pd.to_datetime(data[date_col])
                        found = True
                        break
                if not found:
                    return None
            else:
                data = pd.read_csv(self.csv_path, parse_dates=self.date_col)
        else:
            data = self._generate_fake_data()
        
        if species:
            data = data[data["species"] == species]

        ds = xr.Dataset.from_dataframe(
            data.set_index(["date_collected", "species"])
        ).rename({"date_collected": "time"})
        return ds

    @staticmethod
    def _generate_fake_data():
        """Generates fake seed collection data for testing."""
        species_list = ["Oak", "Maple", "Pine", "Birch", "Spruce"]
        dates = pd.date_range(start="2010-01-01", periods=13, freq="Y")
        data = {
            "date_collected": np.repeat(dates, len(species_list)),
            "species": np.tile(species_list, len(dates)),
            "amount_collected": np.random.randint(5, 30, size=len(dates) * len(species_list))
        }
        return pd.DataFrame(data)
        
        
        
class TrendAnalyzer:
    @staticmethod
    def linear_trend(x, a, b):
        return a * x + b

    def fit_trends(self, ds):
        """Fits linear trends for each species in the dataset."""
        trends = {}

        # Iterate over each species in the dataset
        for species in ds.coords["species"].values:
            # Select the time series for the current species
            time_series = ds.sel(species=species)["amount_collected"]

            # Ensure that time_series is not empty
            if time_series.size == 0:
                print(f"No data for species: {species}")
                continue

            # Create the x values (time in years)
            x = (time_series.time - np.datetime64("2010-01-01")) / np.timedelta64(1, "D")
            x = x / 365.25  # Convert days to years
            y = time_series.values

            # Fit the linear trend
            params, _ = curve_fit(self.linear_trend, x, y)
            trends[species] = (x, y, params)

        return trends

class Plotter:
    def plot_trends(self, trends):
        """Plots trendlines for different species."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        for species, (x, y, params) in trends.items():
            x_fit = np.linspace(x.min().item(), x.max().item(), 100)
            y_fit = TrendAnalyzer.linear_trend(x_fit, *params)
            x_fit_dates = np.datetime64("2010-01-01") + (x_fit * 365.25).astype("timedelta64[D]")
            ax.plot(x_fit_dates, y_fit, linestyle="--", label=f"{species} Trend")
        
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Amount Collected")
        ax.set_title("Seed Collection Trends Over Time")
        ax.legend()
        plt.xticks(rotation=45)
        plt.show()
        print("Plot should be showing")

if __name__ == "__main__":
    print("""
                Welcome to X.R.O.O.T.S
Xarray for Researching Organic Observations in Temporal Systems
    
    Please choose from the following options:
        1. Print raw data
        2. Plot collection over time
        
        3. Exit
    
    """)
    choice = 0
    while choice != '3':
        choice = input("Select option 1 - 3: ")
        
        processor = SeedDataProcessor() 
        ds = processor.load_data()  # Filter by species (optional)

        if choice == "1":
            print(f"/n{ds}/n")
            
        elif choice == "2":
            print("""
            
                1. All Species
                2. Display one species
            
            """)
            
            choice = input("Enter 1 or 2: ")
            if choice == "1":
                print("choice 1")
                analyzer = TrendAnalyzer()
                trends = analyzer.fit_trends(ds)
        
                plotter = Plotter()
                plotter.plot_trends(trends)
            elif choice == "2":
                species = ds.coords["species"]

                for i in range(len(species)):
                    print(f"{i + 1}. {species[i].item()}")

                c = input("Enter the species: ")
                try:
                    ds = processor.load_data(species=species[int(c) - 1])
                    analyzer = TrendAnalyzer()
                    trends = analyzer.fit_trends(ds)

                    plotter = Plotter()
                    plotter.plot_trends(trends)
                except: #fixme
                    print("Wrong. FIXME add data validation")

                
        
        
        
        
    

    
