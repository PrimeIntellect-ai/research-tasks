You are a Machine Learning Engineer preparing training data from a noisy sensor network. You have a dataset located at `/home/user/sensor_data.csv` with features `sensor_1`, `sensor_2`, `sensor_3`, and a binary `target`. Some of the `target` values are missing (represented as empty strings or NaNs).

Your goal is to impute the missing labels using a probabilistic model, generate multiple possible completed datasets via sampling (bootstrapping the missing labels), and then use cross-validation to determine the most robust hyperparameter for a final classification model.

Perform the following steps:
1. **Probabilistic Modeling**: Split the data into labeled (target is not missing) and unlabeled (target is missing) sets. Train a standard Gaussian Naive Bayes model on the labeled data using all three sensor features. Use this model to predict the posterior probability of class 1 ($P(target=1)$) for all unlabeled rows.
2. **Sampling**: Generate 50 possible "completed" datasets. The labeled targets should remain unchanged. For the unlabeled targets, sample a new binary label (0 or 1) for each row based on its predicted posterior probability. 
   *Implementation requirement for reproducibility*: Use `numpy`'s random number generator initialized exactly once with `rng = np.random.default_rng(42)`. For each of the 50 datasets (iterating sequentially from dataset 1 to 50), draw an array of uniform random numbers using `rng.random(size=num_unlabeled)`. For each unlabeled row $i$, if the random number is less than $P(target=1)_i$, assign the label 1; otherwise, assign 0.
3. **Cross-Validation & Hyperparameter Tuning**: For each of the 50 completed datasets, perform Grid Search with 3-fold Stratified Cross-Validation to tune a Logistic Regression classifier (`max_iter=1000`, `random_state=42` for the classifier). Tune the inverse regularization parameter `C` using the grid `[0.01, 0.1, 1.0, 10.0]`. Evaluate using Accuracy and record the best `C` for each of the 50 datasets.

Save your final results in a JSON file at `/home/user/summary.json` with the following exact keys:
- `"avg_posterior_class1"`: The mean of the predicted posterior probabilities of class 1 for all unlabeled rows (as a float, rounded to 4 decimal places).
- `"best_c_mode"`: The `C` value that was selected as the best most frequently across the 50 datasets (as a float). If there is a tie, output the smaller `C`.

Ensure that you process the data and save the final JSON file using a script in the language of your choice.