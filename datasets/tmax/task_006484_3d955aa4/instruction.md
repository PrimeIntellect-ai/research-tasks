You are a data engineer tasked with rewriting a faulty Python ETL pipeline in Rust. The original Python pipeline suffered from a silent upcasting bug where missing integer values (`NaN` in pandas) caused entire columns to be treated as floats, leading to downstream precision issues and memory bloat.

Your goal is to write a robust Rust program that processes a dataset, handles missing values strictly as integers, and performs variance-based feature selection (a form of dimensionality reduction).

Setup:
You have a dataset located at `/home/user/data.csv` containing 5 numerical features (`f1`, `f2`, `f3`, `f4`, `f5`). Some rows have missing values represented by empty strings.

Your Rust program must perform the following:
1. Initialize a new Rust project in `/home/user/etl_rust`.
2. Read the CSV file `/home/user/data.csv`.
3. Impute any missing values in each column with the **median** of the present values in that column. The median must be computed as an integer (if the median falls between two integers, round down to the nearest integer). The columns must remain as integer types.
4. Calculate the population variance for each of the 5 columns after imputation.
5. Perform feature selection: select the 2 features (columns) with the highest population variance.
6. Write the final cleaned and reduced dataset to `/home/user/selected_features.csv`. The output must include the CSV header with the original names of the 2 selected features, followed by the data rows in their original order.

You may use any standard Rust crates (e.g., `csv`, `serde`, `polars`, etc.) by adding them to your `Cargo.toml`. 

Execute your Rust program so that the output file `/home/user/selected_features.csv` is generated successfully.