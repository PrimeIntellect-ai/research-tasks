You are a Data Scientist cleaning a dataset from a faulty batch of sensors.

You have a dataset located at `/home/user/sensor_data.csv` with the following columns:
`sensor_id,val_x,val_y,val_z,status`

Part 1: Tabular Data Cleaning
Using standard bash command-line tools (e.g., `awk`, `grep`, `sed`), filter the dataset to include only the rows where the `status` is `OK`. 
Extract ONLY the numerical measurement columns (`val_x`, `val_y`, `val_z`) for these valid rows and save them as a comma-separated file without a header row at `/home/user/clean_data.csv`.

Part 2: Linear Algebra & Matrix Operations in Rust
Initialize a new Rust project called `data_analyzer` in `/home/user/data_analyzer`.
Configure your Rust project to use the `ndarray` and `csv` crates.

Write a Rust program in this project that:
1. Reads `/home/user/clean_data.csv` into a 2-dimensional matrix $X$ using `ndarray`.
2. Computes the Gram matrix $G = X^T X$ using matrix multiplication.
3. Calculates the trace of the Gram matrix $G$ (the sum of its diagonal elements).
4. Writes the final scalar trace value to `/home/user/trace.txt`, formatted to exactly 2 decimal places (e.g., `123.45`).

Run your Rust program to generate the output file.