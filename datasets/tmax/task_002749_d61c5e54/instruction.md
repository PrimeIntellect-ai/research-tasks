You are a Machine Learning Engineer preparing a dataset for a classification model. You are tired of Python pipelines (like pandas) silently converting integer columns to floats whenever missing values (NaNs) are introduced. You want to build a strict, typesafe ETL pipeline in Rust.

Your task is to write a Rust program that reads two CSV files, performs an inner join, engineers a new feature, imputes missing values strictly as integers, and outputs the final dataset.

Here are the details:
1. **Input Data**: 
   - `/home/user/data/users.csv`: Contains columns `user_id` (integer), `age` (integer, but has missing values represented as empty strings), and `signup_source` (string).
   - `/home/user/data/events.csv`: Contains columns `event_id` (integer), `user_id` (integer), and `score` (float).

2. **Pipeline Requirements**:
   - Create a new Rust project named `strict_etl` in `/home/user/strict_etl`.
   - Read both CSV files. You may use standard crates like `csv` and `serde` (or perform manual parsing if you prefer, as long as it handles the data correctly).
   - Perform an **inner join** on the `user_id` column.
   - **Impute missing data**: Any missing `age` value must be imputed with the integer `0`. Do not allow the `age` column to become a float at any point.
   - **Feature Engineering**: Create a new column `score_normalized` by multiplying the `score` by 10 and rounding to the nearest integer. The result must be an integer type.
   - **Output**: Write the joined and processed data to `/home/user/pipeline_out/dataset.csv`.

3. **Output Format**:
   - The output CSV must have exactly the following header: `event_id,user_id,age,signup_source,score_normalized`.
   - The rows must be sorted in ascending order by `event_id`.
   - Ensure the output directory `/home/user/pipeline_out/` exists.

Write the Rust code, compile it, and run it to produce the final `dataset.csv`.