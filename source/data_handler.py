
"""
Module for handling data fetching and processing for energy consumption analysis.
"""
import requests
import pandas as pd
from pathlib import Path # For multi-platform path handling if saving files

API_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute/records"

class DataHandler:
    """
    Handles fetching, processing, and managing energy consumption data.
    """
    def __init__(self, api_url: str = API_URL):
        """
        Initializes the DataHandler.

        Args:
            api_url (str): The base URL for the data API.
        """
        self.api_url = api_url
        self.dataframe = pd.DataFrame()
        print("DataHandler initialized.")

    def fetch_data_from_api(self, limit: int = 100, offset: int = 0) -> bool:
        """
        Fetches data from the ODRE API.

        Args:
            limit (int): Number of records to fetch.
            offset (int): Offset for pagination.

        Returns:
            bool: True if data fetching was successful, False otherwise.
        """
        params = {
            "limit": limit,
            "offset": offset,
            "order_by": "date_heure DESC" # Get most recent data
        }
        print(f"Fetching data from API: {self.api_url} with params: {params}")
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
            data = response.json()
            
            if 'results' not in data or not data['results']:
                print("No results found in API response.")
                self.dataframe = pd.DataFrame() # Ensure dataframe is empty
                return False

            self.dataframe = pd.DataFrame(data['results'])
            print(f"Data fetched successfully. {len(self.dataframe)} records retrieved.")
            self._process_data()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            self.dataframe = pd.DataFrame() # Ensure dataframe is empty
            return False
        except Exception as e:
            print(f"An unexpected error occurred during API fetch: {e}")
            self.dataframe = pd.DataFrame()
            return False

    def _process_data(self):
        """
        Processes the fetched data.
        - Converts 'date_heure' to datetime objects.
        - Fills NaN values in consumption columns with 0 for plotting.
        """
        if self.dataframe.empty:
            print("No data to process.")
            return

        print("Processing data...")
        if 'date_heure' in self.dataframe.columns:
            self.dataframe['date_heure'] = pd.to_datetime(self.dataframe['date_heure'], errors='coerce')
            self.dataframe.sort_values('date_heure', inplace=True) # Ensure chronological order for plotting
        
        consumption_cols = [
            'consommation_brute_gaz_grtgaz', 'consommation_brute_gaz_terega',
            'consommation_brute_gaz_totale', 'consommation_brute_electricite_rte',
            'consommation_brute_totale'
        ]
        for col in consumption_cols:
            if col in self.dataframe.columns:
                # Convert to numeric, coercing errors to NaN, then fill NaN with 0
                self.dataframe[col] = pd.to_numeric(self.dataframe[col], errors='coerce').fillna(0)
            else:
                print(f"Warning: Expected column '{col}' not found in data. Creating it with 0s.")
                self.dataframe[col] = 0 # Add column if missing to prevent errors later
        
        print("Data processing complete.")

    def get_summary(self) -> str:
        """
        Returns a string summary of the current dataframe.
        """
        if self.dataframe.empty:
            return "No data loaded."
        
        summary = f"Data Summary:\n"
        summary += f"- Total records: {len(self.dataframe)}\n"
        if 'date_heure' in self.dataframe.columns and not self.dataframe['date_heure'].dropna().empty:
            min_date = self.dataframe['date_heure'].min().strftime('%Y-%m-%d %H:%M')
            max_date = self.dataframe['date_heure'].max().strftime('%Y-%m-%d %H:%M')
            summary += f"- Date range: {min_date} to {max_date}\n"
        
        for col in ['consommation_brute_electricite_rte', 'consommation_brute_gaz_totale']:
            if col in self.dataframe.columns:
                total_col = self.dataframe[col].sum()
                mean_col = self.dataframe[col].mean()
                summary += f"- Total {col}: {total_col:,.0f}\n"
                summary += f"- Average {col}: {mean_col:,.0f}\n"
        return summary

    def export_to_csv(self, filepath: str) -> bool:
        """
        Exports the current dataframe to a CSV file.

        Args:
            filepath (str): The path to save the CSV file.

        Returns:
            bool: True if export was successful, False otherwise.
        """
        if self.dataframe.empty:
            print("No data to export.")
            return False
        try:
            path_obj = Path(filepath)
            self.dataframe.to_csv(path_obj, index=False, encoding='utf-8')
            print(f"Data exported successfully to {filepath}")
            return True
        except Exception as e:
            print(f"Error exporting data to CSV: {e}")
            return False

    def get_plot_options(self) -> list:
        """
        Returns a list of available columns for plotting.
        """
        if self.dataframe.empty:
            return ["No data"]
        
        options = [
            'consommation_brute_electricite_rte',
            'consommation_brute_gaz_totale',
            'consommation_brute_totale',
            'consommation_brute_gaz_grtgaz',
            'consommation_brute_gaz_terega'
        ]
        # Return only columns that actually exist in the dataframe
        return [opt for opt in options if opt in self.dataframe.columns]
    