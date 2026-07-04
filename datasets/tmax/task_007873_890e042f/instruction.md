I am a researcher organizing a messy collection of experimental datasets, and I need a Rust-based tool to help me clean them and find similar experiments. 

I have a directory of datasets located at `/home/user/datasets/`. Inside, there are several CSV files (e.g., `alpha.csv`, `beta.csv`, `gamma.csv`) and one specific file named `query.csv`. 

I need you to write and run a Rust program (you can create a Cargo project at `/home/user/dataset_matcher`) that does the following:

1. **Schema Enforcement:** Parse all CSV files in `/home/user/datasets/`. Every file must be parsed to extract the following columns: `sample_id` (String), `temp` (f64), `pressure` (f64), and `yield` (f64).
2. **Missing Value Handling:** 
   - Drop any rows where `sample_id` is empty or missing.
   - For `temp` and `pressure`, if a value is missing or cannot be parsed as a float, impute it using the mean of the valid values for that column *within that specific file* (calculate the mean only from rows that have a valid float for that column and a valid `sample_id`).
3. **Outlier Handling:**
   - After imputation, compute the mean and standard deviation of the `yield` column for each file. 
   - Drop any rows where the `yield` has a z-score greater than 2.0 or less than -2.0. If standard deviation is 0, do not drop any rows.
4. **Linear Algebra & Feature Extraction:**
   - For each cleaned dataset, compute a "characteristic vector" consisting of the final means of the three numerical columns: `[mean(temp), mean(pressure), mean(yield)]`.
5. **Similarity Search:**
   - Treat `query.csv` as the reference.
   - Compute the Cosine Similarity between the characteristic vector of `query.csv` and the characteristic vectors of all other CSV files in the directory.
   - Find the file (excluding `query.csv`) that has the highest cosine similarity to `query.csv`.

Once your Rust program calculates this, it should output a JSON file at `/home/user/recommendation.json` with the following exact format:
```json
{
  "most_similar_dataset": "filename.csv",
  "cosine_similarity": 0.9999
}
```
(Round the cosine similarity to 4 decimal places).

Please create the Rust project, write the code, build it, run it, and ensure the JSON file is generated correctly.