You are a data scientist tasked with cleaning and analyzing a set of noisy sensor readings from an industrial machine. The data is currently scattered across multiple CSV files, and you need to build a reproducible pipeline to join them, manage the storage efficiently, and compute statistical relationships.

In the directory `/home/user/data/`, there are three files:
- `sensor_A.csv` (columns: `timestamp`, `val_A`)
- `sensor_B.csv` (columns: `timestamp`, `val_B`)
- `sensor_C.csv` (columns: `timestamp`, `val_C`)

Your task is to write a Python script at `/home/user/pipeline.py` and run it to perform the following:
1. Load all three CSV files.
2. Perform an **inner join** on the `timestamp` column across all three datasets so that only timestamps present in all three files are retained.
3. Sort the resulting dataset chronologically by `timestamp`.
4. Save this cleaned and joined dataset in Parquet format to `/home/user/cleaned_sensors.parquet` using the PyArrow engine or fastparquet.
5. Compute the Pearson correlation matrix for the columns `val_A`, `val_B`, and `val_C` (in that exact order).
6. Save the resulting 3x3 correlation matrix to a CSV file at `/home/user/correlation.csv`. Format the output to exactly **4 decimal places**. Do not include column headers or row indices in this CSV.

Ensure you install any necessary Python packages (like `pandas`, `pyarrow`, or `fastparquet`) via pip if they are not already installed.