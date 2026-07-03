You are a data analyst tasked with building a custom k-Nearest Neighbors (k-NN) classification tool in C++ from scratch. You have been provided with two files: `/home/user/train.csv` and `/home/user/test.csv`. 

Your objective is to write a C++ program that reads the training data, enforces a strict schema by cleaning the data, performs cross-validation to find the optimal hyperparameter `k`, and then predicts the classes for the test data based on Euclidean distance similarity.

**Step 1: Data Schema Enforcement**
Read `/home/user/train.csv`. The expected schema is a header row `id,label,v1,v2,v3,v4,v5`, followed by data rows. 
- `id`: Integer
- `label`: Integer (0 or 1)
- `v1` to `v5`: Floating point numbers.
You must enforce this schema. If a row is missing columns, contains non-numeric values where numbers are expected, or is otherwise malformed, **discard the entire row**. Keep track of the valid rows in the order they appear.

**Step 2: Cross-Validation & Hyperparameter Tuning**
Implement a k-NN classifier using Euclidean distance. To find the optimal $k$ among $\{1, 3, 5, 7\}$:
- Perform 3-fold cross-validation on your cleaned training dataset.
- Assign rows to folds based on their 0-based index in the *cleaned* dataset using the modulo operator: `fold_id = index % 3`. 
- For each fold $i \in \{0, 1, 2\}$, use rows where `fold_id == i` as the validation set, and the remaining rows as the training set.
- For validation points, compute the Euclidean distance to all points in the training set. Find the $k$ nearest neighbors. If there is a tie in distances, break it by preferring the neighbor with the smaller `id`.
- The predicted label is the majority class among the $k$ neighbors. If there is a tie in the class vote (not possible for odd $k$, but good to consider), default to class 0.
- Calculate the average accuracy across the 3 folds for each $k$.
- Select the $k$ with the highest average accuracy. If there is a tie in accuracy, select the smaller $k$.
- Write the optimal $k$ to a file `/home/user/best_k.txt` (just the integer).

**Step 3: Prediction**
Read `/home/user/test.csv` (assume it is perfectly formatted with header `id,v1,v2,v3,v4,v5`). 
Using the best $k$ found in Step 2, and using the *entire* cleaned training dataset as your reference pool, predict the label for each test instance.
Write the predictions to `/home/user/predictions.csv` with the header `id,label` followed by the predicted values.

Write your C++ code to a file (e.g. `/home/user/solution.cpp`), compile it (e.g., using `g++ -O3 -std=c++17`), and run it to produce the output files.