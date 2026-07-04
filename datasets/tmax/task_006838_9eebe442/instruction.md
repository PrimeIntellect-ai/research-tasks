As an MLOps engineer, you are tracking experiment artifacts from an old automated pipeline. The metadata is split across two files:
1. `/home/user/hyperparameters.csv` - Contains the experiment parameters. Columns: `exp_id,param_a,param_b,param_c`
2. `/home/user/results.csv` - Contains the evaluation metric. Columns: `exp_id,accuracy`

The pipeline had a bug where it occasionally failed to record the accuracy, leaving a literal `"NaN"` string in the CSV. 

Your task is to write a C++ program (at `/home/user/predictor.cpp`) that:
1. **Multi-source Data Joining**: Reads and inner-joins both CSV files on `exp_id`.
2. **Missing Value Handling**: Separates the data into a "labeled" set (valid `accuracy` as a float) and an "unlabeled" set (`accuracy` is `"NaN"`).
3. **Cross-Validation & Hyperparameter Tuning**: Performs Leave-One-Out Cross-Validation (LOOCV) on the *labeled* set to tune `K` for a K-Nearest Neighbors (KNN) regressor. 
   - Search space for `K`: `{1, 2, 3}`.
   - Distance metric: Euclidean distance over `(param_a, param_b, param_c)`. Do not normalize the features.
   - Evaluation metric: Mean Squared Error (MSE).
   - Tie-breaking: If multiple `K` values yield the exact same MSE, choose the smallest `K`.
4. **Similarity Search & Regression**: Using the best `K` and the *entire* labeled dataset as the reference points, predict the `accuracy` for the "unlabeled" experiments. When predicting, the predicted value is the simple average of the `accuracy` of the K nearest neighbors. If there's a distance tie among neighbors when selecting the top K, break ties by selecting the neighbor with the smaller `exp_id`.

Finally, your C++ program should output the results to `/home/user/predictions.txt` in the following exact format:
```
Best K: [K]
[unlabeled_exp_id_1],[predicted_accuracy_1]
[unlabeled_exp_id_2],[predicted_accuracy_2]
...
```
*Note: Sort the predictions by `exp_id` in ascending order. Format predicted accuracies to exactly 2 decimal places.*

Constraints:
- Use standard C++17 (or C++11/14). You may compile it using `g++ -std=c++17 /home/user/predictor.cpp -o /home/user/predictor`.
- You may use any standard library headers.