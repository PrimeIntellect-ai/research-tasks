You are acting as a data analyst. You have been given a custom C-based evaluation tool for a simple 1D threshold classifier, and a dataset in `/home/user/dataset.csv`.

There are two main issues you need to resolve:
1. **Data Integrity Bug**: The provided C code (`/home/user/classifier.c`) calculates the optimal split threshold for a single numerical feature to predict a binary label. However, it suffers from a silent conversion bug (similar to pandas introducing NaNs and converting ints to floats). Specifically, some rows in `dataset.csv` have the string "NaN" in the feature column. The C code uses `atof()`, which silently parses "NaN" as `0.0`, heavily skewing the threshold calculation.
2. **Cross-Validation Setup**: You need to evaluate this model using 5-fold cross-validation, but you currently only have bash tools at your disposal to do the splitting and execution.

Your task:
1. Modify `/home/user/classifier.c` to explicitly ignore (skip) any row where the feature value exactly matches the string "NaN" (do not process it in the training or testing phases).
2. Compile the fixed C program to `/home/user/classifier`.
3. Write a bash script `/home/user/run_cv.sh` that does the following:
   - Strips the header from `/home/user/dataset.csv`.
   - Uses the `split` command to divide the remaining rows into 5 equal parts (there are exactly 100 data rows, so 20 rows per fold). Use the prefix `fold_` for the split files.
   - Loops 5 times. In each iteration $i$ (from 1 to 5), it should use one fold as the test set and concatenate the other 4 folds to form the training set.
   - Runs `./classifier <train_file> <test_file>` for each fold. The C program prints a single float representing the accuracy on the test set.
   - Averages the 5 accuracy scores and writes this final average as a floating-point number (formatted to 2 decimal places, e.g., `0.85`) to `/home/user/final_accuracy.txt`.

Ensure your bash script is fully autonomous and creates the correctly averaged output. Do not change the underlying modeling logic in `classifier.c` other than skipping "NaN" rows.