import pandas as pd

def xlsx_to_csv(xlsx_file_path, output_folder):
    # Read all sheets in the Excel file
    excel_file = pd.ExcelFile(xlsx_file_path)
    
    for sheet_name in excel_file.sheet_names:
        # Load each sheet into a DataFrame
        df = excel_file.parse(sheet_name)
        
        # Define the output CSV file path based on the sheet name
        csv_file_path = f"{output_folder}/{sheet_name}.csv"
        
        # Save the DataFrame to CSV
        df.to_csv(csv_file_path, index=False)
        print(f"Saved {sheet_name} to {csv_file_path}")

# Example usage
xlsx_file_path = 'Tesla_research.xlsx'  # Replace with your Excel file path
output_folder = './'    # Replace with your desired output folder path
xlsx_to_csv(xlsx_file_path, output_folder)