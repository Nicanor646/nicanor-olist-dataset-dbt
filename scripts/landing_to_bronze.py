import os
import duckdb

from pathlib import Path

BASE_QUERY="""
CREATE OR REPLACE TABLE bronze.{table_name} AS 
SELECT * FROM read_csv('{csv_path}', all_varchar=True);
"""

data_root = 'data'
landing_path = 'landing'
bronze_path = 'bronze'

# Replace with your actual directory path
dir_path = Path(os.path.join(data_root,landing_path))

con = duckdb.connect("data/olist.duckdb")
con.execute("CREATE SCHEMA IF NOT EXISTS bronze")

# Loop through all .py files in this folder
for file_path in dir_path.glob("*.csv"):
    print(f"Table name: {file_path.stem}")
    table_name = file_path.stem
    csv_path = str(file_path)
    target_path = (
        csv_path.replace(landing_path, bronze_path)
                .replace('.csv', '.parquet')
    )
    con.execute(BASE_QUERY.format(table_name = table_name,
                                 csv_path = csv_path,
                                 target_path = target_path))

    
