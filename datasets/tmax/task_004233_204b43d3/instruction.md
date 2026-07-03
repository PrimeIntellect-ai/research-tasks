You are a Machine Learning Engineer tasked with preparing a dataset for training. A junior engineer previously wrote a preprocessing script that leaked information from the test set into the training set by applying global mean imputation before splitting the data.

Your task is to implement a correct data preprocessing pipeline in Rust that strictly avoids this data leak.

Here are the requirements:
1. Create a new Rust project called `ml_pipeline` in `/home/user/`.
2. Add necessary dependencies to your `Cargo.toml` (e.g., `csv`, `serde`).
3. Read the dataset located at `/home/user/raw_data.csv`. The dataset has the schema: `id`, `feature_x`, `label`. Some values in `feature_x` are missing (represented as empty strings).
4. Split the data chronologically based on row order: the first 80 rows belong to the training set, and the remaining 20 rows belong to the test set.
5. Calculate the mean of `feature_x` using **strictly the training set** (ignoring missing values).
6. Impute all missing values in `feature_x` for BOTH the training set and the test set using this training mean.
7. Ensure strict data schema enforcement: Output the processed datasets exactly with the headers `id,feature_x,label` and write them to `/home/user/train_processed.csv` and `/home/user/test_processed.csv`.
8. Compile and run your Rust program to generate the output files.

Do not use any external tools (like python or awk) to process the data; all missing value handling, splitting, and schema enforcement must be done within your Rust program.