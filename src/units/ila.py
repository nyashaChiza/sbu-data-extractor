import pandas as pd
from src.base import BluePrint


class ILAUnit(BluePrint):
    """Concrete class implementing BluePrint methods for ILAUnit."""

    def __init__(self, source: str, config: dict):
        """Initialize ILAUnit with data fetched from source."""
        self.data = self.fetch_data(source=source, config=config)
        self.config = config
  

    def fetch_data(self, source: str, config: dict) -> pd.DataFrame:
        """Fetch data from source (currently supports 'excel' only)."""
        if source == 'excel':
            if config.get('path') is None:
                raise ValueError("Path not provided for Excel source in config")
            df = pd.read_excel(config.get('path'))
            return df
        else:
            raise ValueError("Unsupported source")

    def get(self, pk: str):
        """Retrieve data by primary key."""
        try:
            result = self.data.loc[self.data['MANUALPOLICYNO'] == pk]
            if result.empty:
                return {
                    'status': 'failed',
                    'message': f"Policy number '{pk}' not found",
                    'data': None
                }
            else:
                return {
                    'status': 'success',
                    'message': 'success',
                    'data': result.to_dict(orient='records')
                }
        except Exception as e:
            return {
                'status': 'failed',
                'message': str(e),
                'data': None
            }
     
            
    def get_all(self):
        """Retrieve data by primary key."""
        try:
            return {
                    'status': 'success',
                    'message': 'success',
                    'data': self.data.to_dict(orient='records')
                }
        except Exception as e:
            return {
                'status': 'failed',
                'message': str(e),
                'data': None
            }
            
            
    def post(self, data: list):
        """Add new data to the Excel file."""
        try:
            # Check if self.data is a DataFrame
            if not isinstance(self.data, pd.DataFrame):
                raise ValueError("self.data is not a DataFrame")

            # Create a DataFrame from the new data list
            new_data_df = pd.DataFrame(data)
            
            # Concatenate the existing DataFrame and the new data DataFrame
            frames = [self.data, new_data_df]
            self.data = pd.concat(frames, ignore_index=True)
            
            # Save the updated DataFrame back to the Excel file
            self.data.to_excel(self.config['path'], index=False)
            
            return {
                'status': 'success',
                'message': 'Data has been successfully added to the Excel file.',
                'data': data
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'message': str(e),
                'data': data
            }
            
    def update(self, pk: str, update_data: dict):
        """Update a policy in the data source."""
        try:
            # Check if self.data is a DataFrame
            if not isinstance(self.data, pd.DataFrame):
                raise ValueError("self.data is not a DataFrame")

            # Find the index of the row with the specified primary key
            idx = self.data[self.data['MANUALPOLICYNO'] == pk].index

            # Check if the specified primary key exists in the DataFrame
            if idx.empty:
                return {
                    'status': 'failed',
                    'message': f"Policy number '{pk}' not found",
                    'data': None
                }

            # Update the specified columns with the new values
            self.data.loc[idx, list(update_data.keys())] = list(update_data.values())

            # Save the updated DataFrame back to the Excel file
            self.data.to_excel(self.config['path'], index=False)

            return {
                'status': 'success',
                'message': f"Policy with primary key '{pk}' has been successfully updated.",
                'data': None
            }

        except Exception as e:
            return {
                'status': 'failed',
                'message': str(e),
                'data': None
            }

    def delete(self, pk: str):
        """Delete a policy from the data source."""
        try:
            # Check if self.data is a DataFrame
            if not isinstance(self.data, pd.DataFrame):
                raise ValueError("self.data is not a DataFrame")

            # Find the index of the row with the specified primary key
            idx = self.data[self.data['MANUALPOLICYNO'] == pk].index

            # Check if the specified primary key exists in the DataFrame
            if idx.empty:
                return {
                    'status': 'failed',
                    'message': f"Policy number '{pk}' not found",
                    'data': None
                }

            # Delete the row with the specified primary key
            self.data.drop(idx, inplace=True)

            # Save the updated DataFrame back to the Excel file
            self.data.to_excel(self.config['path'], index=False)

            return {
                'status': 'success',
                'message': f"Policy with primary key '{pk}' has been successfully deleted.",
                'data': None
            }

        except Exception as e:
            return {
                'status': 'failed',
                'message': str(e),
                'data': None
            }
