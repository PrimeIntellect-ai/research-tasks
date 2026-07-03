You are a data engineer building an ETL pipeline in Rust. You have a partially completed Rust project at `/home/user/etl_pipeline`. 

The pipeline is supposed to:
1. Read a CSV file from `/home/user/data/input.csv` which has the schema `id,text`.
2. **Handle missing values**: Drop any rows where the `text` field is missing or empty.
3. **Compute 2D embeddings/features**: For each valid text, compute a 2D feature vector:
   - `x`: the length of the string (number of bytes).
   - `y`: the integer average of the ASCII values of the characters (sum of byte values divided by length, rounded down to the nearest integer).
4. **Outlier handling**: Drop any records where the `x` feature (length) is strictly greater than 50.
5. **Experiment tracking & Validation**: Output a JSON file at `/home/user/output/metrics.json` tracking the pipeline's filtering steps. The JSON must exactly match this format:
   `{"missing_dropped": X, "outliers_dropped": Y, "valid_records": Z}`
6. **Plotting**: Generate a scatter plot of the valid `(x, y)` features using the `plotters` crate, saving it to `/home/user/output/scatter.png`. The current code produces a blank image because the drawing backend is misconfigured and drops the drawing context before rendering the points.

Your task is to fix the Rust code in `/home/user/etl_pipeline/src/main.rs`, build the project, and run it successfully so that the accurate `metrics.json` and a correctly rendered `scatter.png` (which must actually contain the plotted points) are produced.

To get started, initialize the Rust project with the necessary dependencies (like `csv`, `serde`, `serde_json`, `plotters`) and write the logic.

The input CSV is already placed at `/home/user/data/input.csv`.
Create the `/home/user/output/` directory if it does not exist.