You are a researcher working on organizing a dataset of sensor logs. Your colleague started writing a Rust program to process the logs but left the project unfinished, and you've noticed a major methodological flaw: their plan would have caused "data leakage" by calculating imputation statistics over the entire dataset before splitting it into training and test sets. 

Your task is to write a Rust command-line tool from scratch that properly prepares the dataset, avoiding data leakage and applying several transformations.

You have been provided a dataset at `/home/user/input.csv` with the following columns: `id`, `text_log`, and `sensor_value`.

Write a Rust project in `/home/user/data_prep` that performs the following steps in order:

1. **Read and Split**: Read `input.csv`. Treat the first 80% of the rows (ordered by appearance) as the Training set, and the remaining 20% as the Test set. 
2. **Tokenization (Feature Engineering)**: For both sets, create a new column called `word_count` which is the number of whitespace-separated words in the `text_log` field.
3. **Missing Value Handling (No Leakage)**: The `sensor_value` column contains missing values (empty strings). Calculate the mean of the `sensor_value` using **only the Training set** (ignoring missing values). Impute (fill) the missing values in *both* the Training and Test sets using this Training mean. Round the imputed value to 4 decimal places.
4. **Outlier Detection**: Calculate the standard deviation (population std dev, n) of the `sensor_value` on the Training set (using pre-imputed known values). Create a new column `is_outlier`. If a row's `sensor_value` (after imputation) is strictly greater than `train_mean + (2 * train_std)` or strictly less than `train_mean - (2 * train_std)`, set `is_outlier` to `1`, otherwise `0`.
5. **Sampling/Bootstrap**: Create a bootstrap sample of your processed Training set. Sample `N` rows with replacement from the processed Training set (where `N` is the size of the Training set). To make this reproducible, use the `rand` crate with `StdRng::seed_from_u64(42)`. (Note: use `rand::seq::SliceRandom` or index generation to pick rows).
6. **Output**: Write three CSV files to `/home/user/`:
   - `/home/user/train_processed.csv` (The processed training set)
   - `/home/user/test_processed.csv` (The processed test set)
   - `/home/user/train_bootstrapped.csv` (The bootstrapped training set)

All output CSVs must contain exactly these columns in order: `id,word_count,sensor_value,is_outlier`.

**Constraints & Setup:**
* You must initialize the Rust project yourself (`cargo new /home/user/data_prep`).
* You can add standard data processing crates like `csv`, `serde`, and `rand` to your `Cargo.toml`.
* Execute your Rust program to generate the files. Ensure the outputs exist and match the requirements.