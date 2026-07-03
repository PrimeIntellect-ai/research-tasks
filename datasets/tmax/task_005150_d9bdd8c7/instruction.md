You are helping a data researcher organize and evaluate a set of 1D spectral datasets. Before deploying a simple baseline model to categorize incoming data streams, the researcher needs to cross-validate its accuracy and benchmark its inference performance in C++.

The model to be tested is a 1D K-Nearest Neighbors (KNN) Regressor. 

You need to write a C++ program at `/home/user/tune_and_benchmark.cpp` that performs hyperparameter tuning, numerical accuracy testing, and performance benchmarking.

### The Dataset
The dataset is located at `/home/user/spectra.csv`. It has a header and four columns: `id,fold,x,y`.
- `id`: Integer identifier.
- `fold`: Integer (1, 2, or 3) indicating the cross-validation fold.
- `x`: Float representing the feature.
- `y`: Float representing the target value.

### Task Requirements
Your C++ program must accept two command-line arguments: the input CSV path, and the output JSON report path.
Example: `./tune_and_benchmark /home/user/spectra.csv /home/user/report.json`

**1. Cross-Validation & Hyperparameter Tuning:**
- Implement a 1D KNN Regressor. The distance between two points is `abs(x_train - x_test)`. 
- To break ties in distance, prefer the point with the smaller `id`. (Hint: stable sort by distance).
- The prediction for a test point is the arithmetic mean of the `y` values of its `K` nearest neighbors.
- Perform 3-fold cross-validation for each $K \in \{1, 3, 5, 7, 9\}$. 
- For each fold $i \in \{1, 2, 3\}$, use the data where `fold != i` as the training set, and the data where `fold == i` as the test set. Calculate the Mean Squared Error (MSE).
- The CV MSE for a given $K$ is the average of the 3 fold MSEs.
- Identify the `best_k` that yields the lowest CV MSE. (If there's a tie in MSE, pick the smaller K).

**2. Inference Performance Benchmarking:**
- Once the `best_k` is found, benchmark its inference speed.
- Train the KNN model using the *entire* dataset (all folds) with `best_k`.
- Measure the time it takes to predict the `y` value for every `x` in the entire dataset. 
- Repeat this full-dataset prediction process 1000 times in a loop.
- Measure the total elapsed time in microseconds for these 1000 iterations.

**3. Output Report:**
Write the results to the specified output JSON file with the following exact keys and format:
```json
{
  "best_k": <integer>,
  "best_cv_mse": <float rounded to 4 decimal places>,
  "benchmark_time_microseconds": <integer>
}
```

Ensure your C++ code is robust, correctly includes necessary headers, compiles with `g++ -O3 -std=c++17`, and handles the CSV parsing properly. Once written, compile and run your code to generate `/home/user/report.json`.