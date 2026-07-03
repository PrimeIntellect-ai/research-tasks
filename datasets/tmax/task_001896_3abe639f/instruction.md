You are helping a data science researcher organize and fix their custom C++ machine learning pipeline. They have implemented a K-Nearest Neighbors (KNN) classifier from scratch for a classification task, along with a K-Fold Cross Validation evaluation loop. 

However, they suspect a **data leakage** bug in their code. Currently, the dataset is being standardized (Z-score normalization) *before* the cross-validation split, meaning information from the validation folds leaks into the training folds.

Your objectives are:

1. **Fix the Data Leakage:** Modify `/home/user/src/pipeline.cpp` so that for each fold in the cross-validation, the `StandardScaler` is fitted **only** on the training set of that fold, and then used to transform both the training and validation sets.
2. **Hyperparameter Tuning:** Update the `main` function to perform hyperparameter tuning. Test the KNN model for \( K \in \{1, 3, 5, 7, 9\} \) using 5-fold cross-validation. Find the \( K \) that yields the highest average cross-validation accuracy. (If there's a tie, pick the smaller \( K \)).
3. **Similarity Search & Prediction:** Using the best \( K \) found, fit the scaler on the **entire** dataset and train the KNN model on the entire dataset. Then, for a new unobserved data point `[1.5, 2.0, -1.0, 0.5]`, find its predicted class and the row indices (0-indexed, based on the original `dataset.csv` order) of its 3 nearest neighbors in the scaled feature space.
4. **Output Format:** Write your final results to `/home/user/results.json` in the exact following format:
```json
{
  "best_k": 3,
  "best_cv_accuracy": 0.85,
  "new_point_prediction": 1,
  "nearest_neighbor_indices": [42, 12, 89]
}
```

**Files Provided:**
- Code: `/home/user/src/pipeline.cpp`
- Data: `/home/user/data/dataset.csv` (Contains 4 continuous features followed by 1 integer class label per row, no header).

You will need to compile your C++ code (e.g., using `g++ -std=c++17 -O3 pipeline.cpp -o pipeline`) and run it to produce the correct JSON output.