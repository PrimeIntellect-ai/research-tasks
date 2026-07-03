You are a Machine Learning Engineer preparing a C++ data pipeline for a recommendation and similarity search system. 

We recently discovered that our previous ETL pipeline had a severe data leakage issue: it was applying feature scaling (Z-score normalization) across the entire dataset *before* splitting it into training and testing sets. This resulted in the test set information bleeding into the training process.

Your task is to write a new C++ pipeline from scratch that correctly prevents this data leakage, runs a basic nearest-neighbor inference, and tracks the experiment metrics.

Write a C++ program at `/home/user/pipeline.cpp` that does the following:
1. **ETL & Data Loading**: Read a CSV dataset located at `/home/user/dataset.csv`. The CSV has a header `id,f1,f2,label` and exactly 100 data rows. The features `f1` and `f2` are floats, and `label` is an integer (0 or 1).
2. **Train/Test Split**: Split the data sequentially. The first 80 rows must be the training set, and the remaining 20 rows must be the test set. Do not shuffle the data.
3. **Leakage-Free Feature Engineering**: Calculate the mean and sample standard deviation for `f1` and `f2` **strictly using the training set**. 
   * Then, apply Z-score standardization `(x - mean) / std` to both the training set and the test set using the training set's mean and standard deviation. 
   * *Formula note: Use the sample standard deviation: `sqrt(sum((x - mean)^2) / (N - 1))`.*
4. **Model Inference (Similarity Search)**: For each item in the test set, find its 1-Nearest Neighbor (1-NN) in the training set using Euclidean distance on the standardized features `(f1, f2)`. Predict the label of the test item as the label of its nearest neighbor. In case of a distance tie, pick the one with the lower `id`.
5. **Experiment Tracking**: Calculate the accuracy of your predictions on the test set. Finally, generate an experiment tracking file at `/home/user/metrics.json` with the following exact structure (values rounded to 4 decimal places):
```json
{
  "train_mean_f1": 0.0000,
  "train_mean_f2": 0.0000,
  "test_accuracy": 0.0000
}
```

Compile and run your C++ program to generate the `metrics.json` file. You may use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<cmath>`, `<string>`, `<sstream>`). Do not use external C++ ML libraries.