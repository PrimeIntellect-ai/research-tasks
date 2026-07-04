You are tasked with cleaning a dataset of noisy numerical sequences and building a C++ program to tune a smoothing model via cross-validation. 

You have a dataset located at `/home/user/data.csv`. It contains 25 rows and no header.
Each row is formatted as: `id,sequence,target`
Example row: `1,3.4|NA|1.2,5.65`

The `sequence` is a string of numbers separated by the pipe character `|`. Some values are missing and represented as the string `NA`.

Your objective is to write and execute a C++ program (`/home/user/tune.cpp`) that does the following:
1. **Tokenization and Preparation:** Read `/home/user/data.csv`. Parse each row. Split the `sequence` string by `|`. Convert the tokens to double precision floats. Any token that is `NA` must be imputed as `0.0`.
2. **Model Formulation:** For a given hyperparameter $w$ (a double), the uncalibrated prediction for a sequence $x$ of length $k$ is calculated as:
   $P_i = \sum_{j=0}^{k-1} x_{i,j} \cdot w^j$
3. **Cross-Validation & Tuning:** We want to tune $w$ to minimize the Mean Squared Error (MSE) using 5-fold cross-validation. 
   - The 25 rows must be split into 5 folds sequentially: Fold 0 is rows 0-4 (0-indexed), Fold 1 is rows 5-9, Fold 2 is rows 10-14, Fold 3 is rows 15-19, and Fold 4 is rows 20-24.
   - For each fold (used as the validation set, 5 rows), the remaining 4 folds (20 rows) act as the training set.
   - On the **training set**, calculate the bias correction term $B$: 
     $B = \frac{1}{20} \sum_{train} (target - P)$
   - On the **validation set**, predict the values using the calibrated model: $\hat{y} = P + B$.
   - Calculate the validation MSE for this fold: $\frac{1}{5} \sum_{val} (target - \hat{y})^2$.
   - The overall CV MSE for a given $w$ is the average of the validation MSEs across all 5 folds.
4. **Grid Search:** Test the following candidate values for $w$: `{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}`.
5. **Output:** Determine which $w$ yields the lowest overall CV MSE. Write the best $w$ and its corresponding CV MSE (rounded to exactly 4 decimal places) to `/home/user/result.txt` in the following format:
   `Best w: 0.X, MSE: Y.YYYY`

Compile your program using `g++ -std=c++17 -O2 /home/user/tune.cpp -o /home/user/tune`, run it, and ensure `/home/user/result.txt` is created with the correct format.