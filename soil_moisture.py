import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class NetCDFProcessor:
    def __init__(self, filepath):
        """Initialize with the path to the NetCDF file."""
        self.filepath = filepath
        self.dataset = None

    def load_data(self):
        """Load the NetCDF file."""
        self.dataset = xr.open_dataset(self.filepath)
        print(self.dataset)  # View dataset structure
        return self.dataset

    def get_soil_temp(self, lat, lon):
        """Extract soil temp data for a given latitude and longitude."""
        if self.dataset is None:
            raise ValueError("Dataset not loaded. Call load_data() first.")
        
        # Find the closest lat/lon index
        lat_idx = np.abs(self.dataset['lat'] - lat).argmin()
        lon_idx = np.abs(self.dataset['lon'] - lon).argmin()

        # Extract soil temp data
        soil_temp = self.dataset['TSOIL1'].isel(lat=lat_idx, lon=lon_idx).values
        return soil_temp


class SoilTempAnalyzer:
    @staticmethod
    def compare_soil_temp(nc_processor, plant_locations):
        """Compare soil temp at given plant locations."""
        results = []
        for lat, lon in plant_locations:
            temp = nc_processor.get_soil_temp(lat, lon)
            results.append((lat, lon, temp))
        return pd.DataFrame(results, columns=["Latitude", "Longitude", "Soil Temp"])


class Plotter:
    @staticmethod
    def plot_soil_temp(nc_processor):
        """Plot the soil temp data as a heatmap."""
        soil_temp = nc_processor.dataset['TSOIL1'].mean(dim='time')  # Averaging over time if available
        plt.figure(figsize=(10, 6))
        soil_temp.plot()
        plt.title("Average Soil temp")
        plt.show()


if __name__ == "__main__":
    netcdf_file = "GEOS.fp.asm.inst1_2d_smp_Nx.20230227_1000.V01.nc4"  # Update with actual file path
    plant_locations = [(35.0, -90.0), (40.0, -100.0)]  # Example lat/lon points
    
    processor = NetCDFProcessor(netcdf_file)
    processor.load_data()
    
    analyzer = SoilTempAnalyzer()
    temp_data = analyzer.compare_soil_temp(processor, plant_locations)
    
    print(temp_data)
    
    plotter = Plotter()
    plotter.plot_soil_temp(processor)
