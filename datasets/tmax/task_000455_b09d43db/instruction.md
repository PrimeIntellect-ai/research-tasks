You are a data scientist reviewing an ETL data pipeline written in C.

In `/home/user/`, you will find two files:
1. `data.csv`: A dataset containing 10 rows of data (plus a header) with columns `id,value,label`.
2. `normalize.c`: A C program that reads `data.csv`, computes the mean and standard deviation of the `value` column, normalizes the values, and splits the data into an 80% training set and a 20% test set. It outputs `/home/user/train_norm.csv` and `/home/user/test_norm.csv`.

There is a critical flaw in `normalize.c`: a "data leak". The normalization statistics (mean and standard deviation) are currently being calculated using the *entire* dataset (train + test), which leaks future test information into the training phase.

Your task:
1. Identify and fix the data leakage bug in `/home/user/normalize.c`. The mean and standard deviation must be calculated using *only* the training set (the first 80% of the rows). 
2. The standard deviation should be the population standard deviation of the training set.
3. Apply these training-derived statistics to normalize *both* the training and test sets.
4. Compile the fixed C code (e.g., `gcc -o normalize normalize.c -lm`) and run it.
5. The program should generate the corrected `/home/user/train_norm.csv` and `/home/user/test_norm.csv`.

Do not change the output file paths, the file formats, or the decimal formatting (`%.4f`). Simply fix the logic, compile, and execute so the correctly normalized CSVs are produced.