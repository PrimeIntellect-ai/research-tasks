You are assisting a researcher who is organizing and evaluating datasets. The researcher has written a custom C pipeline to preprocess a dataset, handle missing values, normalize features, and fit a simple 1D linear regression model to predict a target variable. 

However, the researcher suspects they have inadvertently introduced "data leakage" into their pipeline. Their preprocessing steps (missing value mean-imputation and standardization) are calculating statistics over the *entire* dataset before it is split into training and testing sets, rather than calculating them strictly on the training set and applying those parameters to both sets.

Your task is to:
1. Examine the C source code located at `/home/user/pipeline.c`.
2. Identify and fix the data leakage bug. Specifically, modify the code so that the mean and standard deviation used for imputing missing values (represented by `-999.0`) and normalizing the feature `X` are calculated **only** using the training set. These training statistics must then be used to impute and normalize both the training and testing sets.
3. The dataset is read from `/home/user/data.csv`. The first 80 rows should be used for training, and the remaining 20 rows for testing. (This split logic is already in the file, but in the wrong order relative to preprocessing).
4. Compile your fixed C code using `gcc -O2 -lm pipeline.c -o pipeline`.
5. Run the compiled program. It will output the Mean Squared Error (MSE) on the test set.
6. Write the final computed MSE (exactly as output by the C program) into a file named `/home/user/final_mse.txt`.

Ensure your modifications maintain all original variable types and use the provided mathematical functions. Do not change the random seed or the model fitting logic, only fix the data leakage in the preprocessing phase.