You are an AI assistant helping a data scientist debug a data pipeline written in C.

You have been provided with a dataset at `/home/user/data.csv` and a C program at `/home/user/process.c`. 
The C program reads the dataset, performs bootstrap sampling to create a training set and an Out-Of-Bag (OOB) validation set, and applies z-score normalization (standard scaling) to the features.

**The Bug:**
There is a classic data leakage bug in `process.c`. The program currently computes the mean and standard deviation for each feature using the *entire* dataset *before* splitting it. It then uses these global statistics to scale both the training and OOB sets. This leaks information from the validation set into the training process.

**Your Task:**
1. Modify `/home/user/process.c` to fix the data leakage. 
2. The mean and standard deviation must be calculated *strictly* using the elements of the bootstrap training sample (meaning if a row is sampled 3 times, its values contribute 3 times to the mean and variance). 
3. Use the population standard deviation formula (divide by `N`, not `N-1`). 
4. Apply these train-derived statistics to scale both the bootstrap training sample and the OOB sample.
5. Do NOT modify the custom pseudo-random number generator (`xorshift32`) or the seed/sequence of drawn indices.
6. The program must output the scaled training data to `/home/user/train_scaled.csv`, the scaled OOB data to `/home/user/test_scaled.csv`, and the scaling statistics to `/home/user/stats.txt`. The formats for these files are already implemented in the code; just ensure they receive the correct mathematically-computed values.
7. Compile your fixed program to `/home/user/process` using `gcc /home/user/process.c -o /home/user/process -lm`.
8. Run the compiled program to generate the output files.