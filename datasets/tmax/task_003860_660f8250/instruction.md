You are a data analyst tasked with processing a messy dataset of IoT sensor readings. You must use Rust to enforce a strict data schema, filter out corrupted records, and perform a statistical correlation analysis.

The dataset is located at `/home/user/data/sensors.csv`. It contains a header row and several data rows. Some rows contain malformed data (e.g., strings where floats should be) due to sensor glitches. 

Your tasks are:
1. Create a new Rust project named `sensor_analysis` in `/home/user/sensor_analysis` using Cargo.
2. Write a Rust program that reads `/home/user/data/sensors.csv`. You should use the `csv` and `serde` crates to parse the file.
3. Enforce the following strict schema for the data:
   - `id`: unsigned 32-bit integer (u32)
   - `temperature`: 64-bit float (f64)
   - `humidity`: 64-bit float (f64)
4. Your program must silently ignore (filter out) any row that does not strictly conform to this schema (e.g., where temperature or humidity cannot be parsed as an f64).
5. Calculate the Pearson correlation coefficient between the `temperature` and `humidity` arrays using only the valid rows.
6. Write the final Pearson correlation coefficient, rounded to exactly 4 decimal places (e.g., `0.1234`), to `/home/user/sensor_analysis/correlation.txt`.
7. Run your Rust program to generate the output file.

Do not use any external crates for the Pearson correlation calculation; implement the mathematical formula directly in your Rust code. You may use `csv` and `serde` for data parsing and schema enforcement.