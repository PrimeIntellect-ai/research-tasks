You are an AI assistant helping a Machine Learning engineer prepare a mathematical dataset for training. 

The engineer has a raw dataset of 3D sensor vectors at `/home/user/raw_sensors.csv`. Recently, a downstream Python visualization script has been producing "blank plots" because the data pipeline silently passed through corrupted rows (e.g., strings instead of floats) and zero-magnitude vectors (which cause divide-by-zero errors in the visualization's normalization step).

Your task is to write a robust Rust data preparation pipeline that enforces strict schema validation and filters out these bad records. 

Perform the following steps:
1. Initialize a new Rust project named `data_prep` in `/home/user/data_prep`.
2. Write a Rust program that reads `/home/user/raw_sensors.csv`.
3. The input CSV has a header: `timestamp,x,y,z`.
4. Enforce the following schema and data rules:
   - `timestamp` must be a String.
   - `x`, `y`, and `z` must be strictly parsable as 64-bit floating point numbers (`f64`). 
   - If a row fails to parse into these types, drop it entirely (do not panic, just skip it).
5. For each valid row, calculate the L2 norm (Euclidean magnitude) of the vector (x, y, z). The formula is: `sqrt(x^2 + y^2 + z^2)`.
6. To fix the "blank plot" bug, drop any row where the calculated L2 norm is exactly `0.0`.
7. Write the resulting valid records to a new CSV file at `/home/user/clean_norms.csv` with the header `timestamp,norm`. Format the `norm` to exactly 4 decimal places (e.g., `3.0000`).

You may use third-party crates like `csv` and `serde` in your `Cargo.toml`. Make sure to compile and run your program so that `/home/user/clean_norms.csv` is correctly generated.