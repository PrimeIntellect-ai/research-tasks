I'm a data analyst working on processing CSV files to calculate a risk score for customer records. I previously had a Python script that processed this, but it silently failed due to a misconfiguration (it performed integer division on features, resulting in "blank" or zeroed-out scores for everyone, much like a plotting library producing blank plots when the backend is missing). 

I want to rebuild this pipeline in **Rust** to ensure type safety and include a reproducibility test.

Please create a new Rust project called `risk_pipeline` in `/home/user/` and write a tool that does the following:

1. **Package Setup**: Create a Cargo project at `/home/user/risk_pipeline`. You will need to install and configure dependencies to read and write CSV files (e.g., `csv` and `serde` crates).

2. **Data Ingestion**: Read the input dataset located at `/home/user/data/records.csv`. It has the following columns: `id` (integer), `age` (integer), `income` (integer), `category` (string: 'A', 'B', or 'C').

3. **Feature Engineering**:
   - Normalize `age`: `age_norm = age / 100.0`
   - Normalize `income`: `income_norm = income / 100_000.0`
   - One-hot encode `category`: 
     - `is_A = 1.0` if category is 'A', else `0.0`
     - `is_B = 1.0` if category is 'B', else `0.0`
     - (Category 'C' is the baseline, so it contributes 0.0 to both).

4. **Regression Scoring**:
   Apply the following pre-trained linear regression formula to compute the score:
   `score = (0.5 * age_norm) + (2.0 * income_norm) + (1.2 * is_A) - (0.5 * is_B)`

5. **Reproducibility Testing**:
   Inside your Rust code (e.g., in `src/main.rs`), write a unit test named `test_reproducibility` that programmatically verifies the feature engineering and scoring logic. It should assert that a record with `age=50`, `income=50000`, and `category=A` produces exactly a score of `2.450`. 

6. **Output**:
   The program must write the results to `/home/user/risk_pipeline/predictions.csv` with exactly two columns: `id` and `score`. 
   Format the `score` to exactly 3 decimal places (e.g., `2.525`).

Please run your code to generate the `predictions.csv` file, and also make sure to run `cargo test` to verify your reproducibility test passes.