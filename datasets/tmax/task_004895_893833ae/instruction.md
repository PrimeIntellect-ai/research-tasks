You are a Machine Learning Engineer preparing training data and building a baseline model evaluator. 

We need to implement a lightweight K-Nearest Neighbors (KNN) regressor in purely standard C to tune a hyperparameter using K-Fold Cross-Validation. 

Your tasks are to:
1. **Preprocess the Data**: Read the dataset from `/home/user/data.csv`. The CSV has 100 rows and 4 columns (comma-separated). The first 3 columns are features (X0, X1, X2) and the last column is the target variable (Y). First, perform basic linear algebra/statistics to standardize the 3 feature columns across the entire dataset (transform each feature to have a mean of 0 and a population standard deviation of 1). Do not standardize the target Y.
2. **Implement K-Nearest Neighbors Regressor**: Write a function to predict the target using the average of the `K` nearest neighbors based on the Euclidean distance of the standardized features.
3. **Cross-Validation & Hyperparameter Tuning**: Implement 5-fold cross-validation (sequential splits: fold 0 is rows 0-19, fold 1 is rows 20-39, etc.) to evaluate `K` values in the set {1, 2, 3, 4, 5}. 
4. Calculate the Mean Absolute Error (MAE) for each `K` across all 5 folds.
5. Identify the `K` that yields the lowest average MAE.

Write your solution in a single C file at `/home/user/knn_cv.c`. Compile it and run it. 
Your program must output a JSON file at `/home/user/best_model.json` with the exact following format:
`{"best_k": 3, "best_mae": 1.23}`
(Ensure the MAE is rounded to 2 decimal places).

No external machine learning libraries or non-standard C math libraries (other than `<math.h>`, `<stdlib.h>`, `<stdio.h>`, etc.) are allowed.