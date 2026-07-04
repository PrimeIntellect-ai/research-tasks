You are a data analyst taking over a C++ project. A previous team member wrote a script, `/home/user/data_processor.cpp`, to clean a dataset located at `/home/user/dataset.csv`. 

The dataset contains 1000 rows with columns: `id,category,measurement`. 
The `measurement` column has missing values (represented as `-999.0`). 

The current C++ program performs the following pipeline:
1. Reads the CSV.
2. Calculates the mean and standard deviation of the `measurement` column (ignoring the missing values).
3. Imputes the missing values with the calculated mean.
4. Normalizes all `measurement` values using Z-score normalization: `(value - mean) / std_dev`.
5. Splits the data into a Train set (first 800 rows) and a Test set (remaining 200 rows).
6. Writes the outputs to `/home/user/train_clean.csv` and `/home/user/test_clean.csv`.

**The Problem:**
The script suffers from **data leakage**. It calculates the mean and standard deviation over the *entire* dataset before splitting it. Because the Test set is supposed to represent unseen future data, it should not influence the imputation or normalization statistics.

**Your Task:**
1. Fix the data leak in `/home/user/data_processor.cpp`. 
2. Modify the code so that the mean and standard deviation are calculated **only** using the Train set (the first 800 rows).
3. Use this *Train mean* and *Train standard deviation* to impute missing values and normalize the measurements for **both** the Train and Test sets.
4. Compile the fixed C++ code into an executable named `/home/user/process` (e.g., `g++ -O3 /home/user/data_processor.cpp -o /home/user/process`).
5. Run the executable to generate the corrected `/home/user/train_clean.csv` and `/home/user/test_clean.csv`. 

The output CSVs must retain the original header (`id,category,measurement`) and the `measurement` values should be printed to exactly 4 decimal places.