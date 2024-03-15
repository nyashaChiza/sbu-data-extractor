import os
from src.units import ILAUnit

def main():
    # Fetch the path to the Excel file that contains master data
    excel_file = ""
    path = os.path.join(os.getcwd(), 'src', 'data', excel_file)
    
    # Configure the ILAUnit with the path
    config = {'path': path}
    unit = ILAUnit(source='excel', config=config)
    
    # Retrieve all data
    data = unit.get_all()
    print(data)

if __name__ == "__main__":
    main()
