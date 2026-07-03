You are an AI assistant helping a Machine Learning Engineer fix a data preparation pipeline written in C++.

The engineer has written an ETL pipeline (`/home/user/pipeline.cpp`) that reads a dataset of embeddings (`/home/user/data/embeddings.csv`), normalizes the features (Z-score standardization), and then splits the data into a Training set and a Test set (80% train, 20% test). 

However, they realized there is a critical **data leak**: the pipeline computes the mean and standard deviation for normalization over the *entire* dataset before splitting. This allows information from the test set to leak into the training features.

Your tasks are:
1. **Fix the C++ pipeline:** Modify `/home/user/pipeline.cpp` so that it correctly prevents data leakage. The pipeline must:
   - Read the 100 rows from `/home/user/data/embeddings.csv` (each row has 3 floating-point features).
   - Perform the split *first*: the first 80 rows are the Training set, and the remaining 20 rows are the Test set.
   - Compute the feature-wise mean and population standard deviation ($\sigma = \sqrt{\frac{\sum (x - \mu)^2}{N}}$) using **only** the Training set.
   - Standardize both the Training and Test sets using the mean and standard deviation computed from the Training set.
   - Save the normalized training data to `/home/user/train_norm.csv` and the normalized test data to `/home/user/test_norm.csv` (comma-separated, 6 decimal places).

2. **Compile and Run:** Compile your fixed C++ code into an executable at `/home/user/pipeline` and run it. You may use `g++ -std=c++17` to compile.

3. **Hypothesis Testing (Confidence Interval):** After correctly applying the training statistics to the test set, the test set features will no longer have exactly a mean of 0. Write a script (C++ or Python) to compute the 95% Confidence Interval for the mean of the **first feature (column 0)** of the normalized Test set (`/home/user/test_norm.csv`). 
   - Use the t-distribution for your critical value (for N=20, df=19, $t \approx 2.093$).
   - The formula is: $CI = \bar{x} \pm t \cdot \frac{s}{\sqrt{N}}$, where $s$ is the *sample* standard deviation of the test feature.
   - Save the confidence interval to `/home/user/ci_output.txt` in the exact format: `[lower_bound, upper_bound]` rounded to 4 decimal places.

Make sure all output files are exactly at the specified paths.