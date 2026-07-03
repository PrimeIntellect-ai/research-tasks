You are a data engineer tasked with building a robust ETL (Extract, Transform, Load) pipeline in C. 

We have two datasets: `/home/user/train.csv` and `/home/user/test.csv`. These files contain numeric sensor data with 2 features (columns) separated by commas. Missing values are represented by the sentinel value `-9999.0`.

A previous engineer wrote a Python script for this, but introduced a severe data leakage bug by calling `fit_transform` on the entire dataset at once (train and test combined). To speed up the pipeline and fix the leakage, you must implement the ETL processor in C from scratch.

Your task is to write a C program `/home/user/etl_processor.c` that performs the following operations:
1. **Missing Value Imputation:** Calculate the mean of each column using *only* the valid data in `train.csv` (ignore `-9999.0` when computing the sum and count). Impute (replace) all missing values in BOTH `train.csv` and `test.csv` with the corresponding column mean from the *train* dataset.
2. **Z-score Normalization (Standardization):** After imputation, calculate the standard deviation (population standard deviation, divide by $N$) of each column in the imputed *train* dataset. Then, normalize both `train.csv` and `test.csv` by subtracting the train mean and dividing by the train standard deviation.
3. **Data Leakage Prevention:** Crucially, statistics (mean and standard deviation) used for transforming the test set *must* be derived entirely from the training set to prevent data leakage.
4. **Output:** The program should read `/home/user/train.csv` and `/home/user/test.csv`, and write the processed matrices to `/home/user/train_processed.csv` and `/home/user/test_processed.csv`. Print floating point numbers to exactly 4 decimal places (e.g., `%.4f`), separated by commas.

Compile your program (e.g., `gcc -o etl_processor etl_processor.c -lm`), run it, and ensure the processed CSV files are created successfully in `/home/user/`.