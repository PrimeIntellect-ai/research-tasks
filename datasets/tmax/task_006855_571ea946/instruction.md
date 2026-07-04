You are a data engineer working on a C++ ETL and inference pipeline. You have been given a C++ program, `/home/user/process_data.cpp`, which reads a binary dataset `/home/user/dataset.bin`. 

The dataset contains 12,000 samples, each consisting of a 5-dimensional feature vector of 32-bit floats. 
The pipeline performs two tasks:
1. Normalizes the features using z-score standardization (subtracting the mean and dividing by the population standard deviation).
2. Runs inference using a simple pre-trained linear model on the normalized data, and saves the predictions.

**The Bug:**
There is a serious data leakage bug in `process_data.cpp`. The feature means and standard deviations are currently being computed over the *entire* dataset (all 12,000 samples). In reality, the first 10,000 samples constitute the training set, and the remaining 2,000 are the test set. 

**Your Task:**
1. Fix the data leakage bug in `/home/user/process_data.cpp`. Modify the code so that the mean and standard deviation for each of the 5 features are calculated **only** using the first 10,000 samples (the training set). Note: Use population standard deviation (divide by N=10000).
2. The normalization step must apply these training statistics to normalize the entire dataset (both train and test sets).
3. The inference step (which applies weights and bias) should remain unchanged, but you must ensure that the predictions for the **test set only** (the last 2,000 samples) are written to `/home/user/test_predictions.txt`.
4. Ensure the output in `/home/user/test_predictions.txt` contains exactly 2,000 lines, with one prediction per line, formatted to exactly 4 decimal places.
5. Compile and run your fixed C++ program to generate the output file.

You can use `g++` to compile the code.