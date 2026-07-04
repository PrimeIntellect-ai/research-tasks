You are a machine learning engineer tasked with implementing and tuning a custom Ridge Regression model from scratch in C++. You need to set up the numerical environment, implement cross-validation, and perform hyperparameter tuning.

Your objective:
1. Create a working directory at `/home/user/ml_prep`.
2. Download and extract the Eigen 3.4.0 library (a C++ template library for linear algebra) into `/home/user/ml_prep/eigen` so that its headers are accessible at `/home/user/ml_prep/eigen/Eigen`. (Hint: you can download it from `https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz`).
3. Write a C++ program at `/home/user/ml_prep/tune_ridge.cpp` that:
   - Generates a synthetic dataset of 100 samples. The input feature $x_i$ should be the integer index $i$ for $i \in \{0, 1, \dots, 99\}$. The target variable should be $y_i = 2.5 \cdot x_i + 10$.
   - Constructs the design matrix $X$ of size $100 \times 2$, where the first column is all 1s (intercept) and the second column is $x_i$.
   - Implements K-Fold cross-validation with $K=5$. The folds must be strictly sequential (Fold 1: indices 0-19 as validation, 20-99 as train; Fold 2: indices 20-39 as validation, rest as train, etc.).
   - Evaluates Ridge Regression for the hyperparameters (regularization strength) $\lambda \in \{0, 10, 100, 1000\}$.
   - The Ridge Regression closed-form solution is $\beta = (X_{train}^T X_{train} + \lambda I)^{-1} X_{train}^T y_{train}$. (Note: apply the penalty $\lambda$ to all parameters, including the intercept, for simplicity).
   - Computes the average Mean Squared Error (MSE) across the 5 validation folds for each $\lambda$.
4. The C++ program should find the $\lambda$ that minimizes the average validation MSE and write the result to `/home/user/ml_prep/tuning_results.txt` exactly in this format:
```
Best lambda: <lambda>
Best MSE: <mse>
```
(Format MSE to 4 decimal places).

5. Create a bash script `/home/user/ml_prep/run_pipeline.sh` that compiles `tune_ridge.cpp` (using `g++`, ensuring the Eigen headers are in the include path) and runs the compiled executable.

Execute your bash script to produce the final `tuning_results.txt`.