You are an automation specialist tasked with building a high-performance data processing pipeline to clean, impute, and store sensor data.

We have a large dataset of sensor readings located at `/home/user/sensor_data.csv`. The data contains three columns: `sensor_id` (string), `timestamp` (integer), and `value` (float). Unfortunately, the network drops packets frequently, resulting in many missing `value`s (represented as empty strings in the CSV).

Your goal is to build a Rust-based multi-stage pipeline that does the following:

1. **Fix the Vendored Dependency:** 
   Our pipeline relies on a locally vendored version of the PistonDevelopers `interpolation` crate, located at `/app/interpolation`. However, someone recently modified it, and its linear interpolation function (`lerp`) is currently producing wildly incorrect results. You must find and fix the mathematical perturbation in the `interpolation` crate source code.

2. **Parallel Imputation (Rust):**
   Write a Rust program (you can initialize a Cargo project at `/home/user/imputer`) that reads `/home/user/sensor_data.csv`.
   - The program must process each `sensor_id` in parallel.
   - For each sensor, sort the records by `timestamp`.
   - Impute the missing `value`s using linear interpolation (via the fixed `interpolation` crate) based on the nearest surrounding valid points in time.
   - Write the fully gap-filled dataset to `/home/user/cleaned_data.csv` (keeping the same header: `sensor_id,timestamp,value`).

3. **Database Bulk Import:**
   Using bash tools and the `sqlite3` CLI, bulk load `/home/user/cleaned_data.csv` into a SQLite database at `/home/user/sensors.db`.
   - The table must be named `readings`.
   - The schema must be: `sensor_id TEXT, timestamp INTEGER, value REAL`.

Constraints:
- The missing values must be interpolated accurately. An automated test will measure the Mean Squared Error (MSE) of your imputed values against the ground truth continuous function.
- You must use Rust as the primary language for the data processing step. 
- You may use crates like `csv`, `rayon`, and the local `/app/interpolation` in your `Cargo.toml`.