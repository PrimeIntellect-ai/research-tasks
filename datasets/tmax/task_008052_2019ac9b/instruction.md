You are a data engineer building a reproducible ETL pipeline in Rust.

We have a 3D sensor data file located at `/home/user/sensor_data.csv` (no header, three comma-separated f32 values per row representing X, Y, Z). 
Your task is to write a Rust program that performs dimensionality reduction (via a linear projection) and sequential Bayesian updating, and then wrap this in a bash script for reproducible execution.

Step 1: Write a Rust project in `/home/user/etl/`.
The program should read `/home/user/sensor_data.csv` line by line.
For each line:
1. Parse the three values as 32-bit floats (`x`, `y`, `z`).
2. Project this 3D vector into a 1D scalar observation `v` using the dot product with the vector `W = [0.5, 0.5, 0.707]`.
   So, `v = 0.5*x + 0.5*y + 0.707*z`.
3. Treat `v` as an observation to update a Gaussian belief of the system's state.
   The initial prior belief has mean `mu = 0.0` and variance `var = 1.0`.
   The observation model has a known, constant variance `var_v = 2.0`.
   Update the belief sequentially for each row using the standard Gaussian posterior formulas:
   `new_mu = (mu * var_v + v * var) / (var + var_v)`
   `new_var = (var * var_v) / (var + var_v)`

Step 2: Write the final output.
After processing all rows, the Rust program must write a single line to `/home/user/output.txt` in the exact following format (rounded to 4 decimal places):
`Final State: mu={mu}, var={var}`

Step 3: Create a reproducible pipeline script.
Write an executable bash script at `/home/user/run.sh` that compiles the Rust project in release mode and executes it to produce the `output.txt` file.

You must build the Rust project from scratch or initialize it yourself in `/home/user/etl`. Ensure `run.sh` succeeds and correctly generates `/home/user/output.txt`.