You are an algorithmic data scientist working on a C-based custom machine learning pipeline. You have inherited a project that processes tabular data, normalizes it, and applies a pre-trained linear regression model to make predictions.

However, the pipeline has a critical flaw: a data leakage bug. The current C program computes the normalization statistics (mean and standard deviation) using the *entire* dataset (both training and testing data combined) before applying them. This violates the strict separation of train and test sets, as the test set's distribution "leaks" into the training feature scaling.

Your task has three phases:

1. **Data Preprocessing**:
   You have a raw dataset at `/home/user/raw_data.csv` with a header `f1,f2,f3,target`. 
   Using standard CLI tools, clean this dataset by removing any rows that contain the string `NA`. 
   Save the first 100 valid data rows (excluding the header) to `/home/user/train.csv`.
   Save the remaining valid data rows to `/home/user/test.csv`.

2. **Fixing the Data Leak (C Programming)**:
   The inference pipeline is located at `/home/user/pipeline.c`. 
   Modify this C program so that it calculates the mean and standard deviation for normalization **strictly using the training set**. These training statistics must then be used to normalize *both* the training set and the test set. (Do not change the pre-trained weights or the inference logic).

3. **Compilation and Validation**:
   Compile the fixed C program using `gcc` into an executable named `/home/user/pipeline`.
   Run the executable. It is designed to read `train.csv` and `test.csv`, apply the fixes, and print the resulting predictions for the test set to standard output.
   Save the program's output to `/home/user/test_predictions.txt`.

Ensure your final predictions file `/home/user/test_predictions.txt` contains exactly the predicted float values for the test set, one per line, with 4 decimal places (as formatted by the C program).