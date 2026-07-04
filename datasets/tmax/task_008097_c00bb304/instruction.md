You are helping a data science researcher who is building a custom C-based pipeline for dataset preprocessing. 

The researcher has an embeddings dataset located at `/home/user/data/embeddings.csv`. There are 10 rows in this dataset. The first 8 rows are the training set, and the last 2 rows are the test set.

They have written a program `/home/user/src/normalize.c` that reads this CSV, normalizes the features (Min-Max scaling to the range [0, 1]), and splits the output into `/home/user/out/train_scaled.csv` and `/home/user/out/test_scaled.csv`.

However, the researcher noticed their downstream classification model has suspiciously high accuracy on the test set. They have inadvertently introduced a **data leak**: the current C code computes the minimum and maximum values for scaling across the *entire* dataset (all 10 rows) before applying the scaling and splitting the data.

Your task is to:
1. Fix the data leak in `/home/user/src/normalize.c`. Modify the code so that the minimum and maximum values for each feature are computed **only** on the training set (the first 8 rows).
2. The scaling must still be applied to *all* rows (both train and test) using the `min` and `max` derived exclusively from the training set. 
3. Compile the fixed program: `gcc /home/user/src/normalize.c -o /home/user/src/normalize`
4. Run the program to generate the corrected `/home/user/out/train_scaled.csv` and `/home/user/out/test_scaled.csv`.
5. Compute the **sample covariance** (divide by N-1) between Feature 0 (the first column) and Feature 1 (the second column) of the newly generated `test_scaled.csv`.
6. Save this single sample covariance value to `/home/user/out/test_covariance.txt`, rounded to 4 decimal places.

All output files should be strictly comma-separated. Do not use any external C libraries beyond the standard library.