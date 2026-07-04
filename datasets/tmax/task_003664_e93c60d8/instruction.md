You are a data analyst working on approximating a legacy scoring engine. A stripped binary of the legacy engine is provided at `/app/oracle`. It takes a CSV file containing 5 numerical columns (comma-separated, no header) as a command-line argument and prints a target score to standard output (one float per line).

Your objective is to:
1. Generate a sufficiently large training dataset of 5-dimensional feature vectors.
2. Query the `/app/oracle` to obtain the ground truth scores for your dataset.
3. Write a C++ program that performs tabular data transformation and trains a Ridge Regression model to approximate the oracle. You must implement k-fold cross-validation to select the optimal L2 regularization penalty (`lambda`) from a set of your choosing.
4. Track your cross-validation experiment results by writing a summary to `/home/user/cv_results.log` (format: `lambda, mean_validation_mse`).
5. Write your final inference code in `/home/user/predictor.cpp` and compile it to `/home/user/predictor`.

Requirements for `/home/user/predictor`:
- It must take a single command-line argument: the path to an input CSV file (5 columns, no header).
- It must output the predicted scores to standard output, one per line.
- You may use the Eigen library (available at `/usr/include/eigen3`) for linear algebra operations.
- Do not use any external machine learning libraries (like mlpack or dlib); you must implement the Ridge Regression math using Eigen.

We will evaluate your `/home/user/predictor` against the `/app/oracle` on a hidden dataset of 10,000 rows. The Mean Squared Error (MSE) between your predictions and the oracle's outputs must be less than `0.01`.