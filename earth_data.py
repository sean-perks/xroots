import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings


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

    def get_data_at_coordinate(self, lat, lon, data_variable):
        """Extract soil data for a given latitude and longitude."""
        if self.dataset is None:
            raise ValueError("Dataset not loaded. Call load_data() first.")

        # Find the closest lat/lon index
        lat_idx = np.abs(self.dataset['lat'] - lat).argmin()
        lon_idx = np.abs(self.dataset['lon'] - lon).argmin()

        # Extract soil temp data
        data = self.dataset[data_variable].isel(lat=lat_idx, lon=lon_idx).values
        return data

    def choose_data_variable(self, prompt="Enter the number associated with the variable you choose: "):
        vars = list(self.dataset.data_vars)
        response = -1
        print([str(i) for i in range(len(vars) + 1)])
        while response not in [str(i) for i in range(1, len(vars) + 1)]:
            c = 1
            for v in vars:
                print(f"{c}.  {v}")
                c += 1
            print("\n(x)  Quit!\n")
            response = input(prompt)
            if response.lower() == 'x':
                print("Goodbye")
                quit()

        return vars[int(response)-1]


class Analyzer:
    @staticmethod
    def compare_data(nc_processor, plant_locations, data_variable = None):
        """compare soil temp at given plant locations.
        plant locations is list of lat/lon tuples: [(35, -90), (40, -100), ...]
        """
        if not data_variable:
            data_variable = nc_processor.choose_data_variable()
        results = []
        for lat, lon in plant_locations:
            try:
                temp = nc_processor.get_data_at_coordinate(lat, lon, data_variable)
                results.append((lat, lon, temp))
            except ValueError as e:
                error = "Function will return None instead of pd.DataFrame: " + str(e)
                warnings.warn(error)
                return None
        return pd.DataFrame(results, columns=["Latitude", "Longitude", data_variable])


class Plotter:
    @staticmethod
    def plot_data(nc_processor, data_variable = None):
        """Plot the soil temp data as a heatmap."""
        if not data_variable:
            data_variable = nc_processor.choose_data_variable()
        data = nc_processor.dataset[data_variable].mean(dim='time')  # Averaging over time if available
        plt.figure(figsize=(10, 6))
        try:
            data.plot()
            plt.title(data_variable)
            plt.show()
        except TypeError as e:
            error = str(e)
            warnings.warn(error)


if __name__ == "__main__":
    netcdf_file = "data\GEOS.fp.asm.inst1_2d_smp_Nx.20230227_1000.V01.nc4"
    plant_locations = [(35.0, -90.0), (40.0, -100.0)]  # example lat/lon points

    processor = NetCDFProcessor(netcdf_file)
    processor.load_data()

    analyzer = Analyzer()
    temp_data = analyzer.compare_data(processor, plant_locations)
    print(temp_data)

    plotter = Plotter()
    plotter.plot_data(processor)
