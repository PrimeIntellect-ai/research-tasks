You are an MLOps engineer tasked with fixing and benchmarking a data processing pipeline written in Rust. 

The pipeline processes a raw dataset, handles missing values and outliers, performs feature engineering, and applies dimensionality reduction (by dropping unnecessary features). However, the current Rust implementation has several logical bugs.

Your task is to fix the pipeline, run it, and track the experiment artifacts.

Here is the setup:
- A Rust project is located at `/home/user/pipeline`
- The input dataset is at `/home/user/raw_data.csv`

The pipeline is supposed to do the following:
1. **Missing Value Handling**: Impute missing values in the `f1` column with the **mean** of the valid `f1` values.
2. **Outlier Handling**: Remove any rows where the `f2` column is an outlier, defined strictly as `f2 > 100.0`.
3. **Feature Engineering**: Create a new feature `f_new` which is the product of `f1` and `f2`.
4. **Dimensionality Reduction**: Keep ONLY the `f_new` and `f3` columns in the final dataset (in that exact order).
5. **Output**: Save the processed dataset to `/home/user/processed_data.csv`.

Currently, the code in `/home/user/pipeline/src/main.rs` incorrectly imputes missing values with `0.0`, removes rows where `f2 < 100.0`, and fails to drop `f4`.

**Instructions:**
1. Fix the bugs in `/home/user/pipeline/src/main.rs` so it implements the logic described above.
2. Build the project in release mode (`cargo build --release`).
3. Run the compiled binary to generate `/home/user/processed_data.csv`.
4. Create an experiment tracking artifact at `/home/user/experiment_artifact.json` containing the final number of rows and the mean of the `f_new` column. The file must be exactly in this format:
```json
{
  "rows": <integer>,
  "f_new_mean": <float rounded to 2 decimal places>
}
```