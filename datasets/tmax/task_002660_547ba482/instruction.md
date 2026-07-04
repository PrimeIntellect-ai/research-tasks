You are an MLOps engineer tasked with analyzing the artifacts of an A/B test between two experimental models (Model A and Model B). The training platform crashed before calculating the validation metrics, leaving behind only fragmented artifacts. 

Your task is to write a Python script that reconstructs the models, runs inference, joins the results, and performs both frequentist and Bayesian statistical analyses to evaluate the experiment.

The artifacts are located in `/home/user/experiment/`:
1. `val_features.csv` - Contains validation features. Columns: `id, f1, f2, f3`.
2. `val_labels.json` - Contains ground truth labels mapping `id` (as a string) to `label` (0 or 1).
3. `model_A_arch.json` & `model_A_weights.npz` - Architecture definition and NumPy arrays (`W0`, `b0`, etc.) for Model A.
4. `model_B_arch.json` & `model_B_weights.npz` - Architecture definition and NumPy arrays for Model B.

**Requirements:**

1. **Model Reconstruction & Inference**:
   - Parse the JSON architecture files. They define a sequence of layers (e.g., `{"layers": [{"type": "linear", "in": 3, "out": 4}, {"type": "relu"}, ...]}`).
   - Load the corresponding weights from the `.npz` files. The keys in the `.npz` file will be `W0`, `b0` for the first linear layer, `W1`, `b1` for the second, etc.
   - Implement a simple NumPy-based forward pass for these multi-layer perceptrons. Supported activations: `relu` ($max(0, x)$) and `sigmoid` ($1 / (1 + e^{-x})$).
   - Generate predictions for all records in `val_features.csv`. A predicted probability $\ge 0.5$ should be considered class 1, otherwise 0.

2. **Data Joining & Accuracy Calculation**:
   - Join your predictions with the ground truth labels from `val_labels.json` using the `id` field.
   - Calculate the raw accuracy (correct predictions / total samples) for both Model A and Model B.

3. **Hypothesis Testing**:
   - Perform a standard 2-proportion Z-test to compare the accuracies of Model A and Model B. Compute the two-sided p-value. (You may use `statsmodels.stats.proportion.proportions_ztest`).

4. **Bayesian Inference**:
   - Model the accuracy of each model using a Beta-Binomial conjugate model.
   - Assume an uninformative uniform prior for the accuracy of both models: $Beta(\alpha=1, \beta=1)$.
   - Calculate the exact posterior distribution parameters ($\alpha_{post}$, $\beta_{post}$) for both Model A and Model B based on their correct and incorrect predictions.

**Output:**
Your script must write the final analysis to `/home/user/experiment_results.json` strictly using this format:
```json
{
  "accuracy_A": 0.00,
  "accuracy_B": 0.00,
  "p_value_ztest": 0.0000,
  "bayesian_posterior": {
    "model_A": {
      "alpha": 0,
      "beta": 0
    },
    "model_B": {
      "alpha": 0,
      "beta": 0
    }
  }
}
```
Round `accuracy_A` and `accuracy_B` to 4 decimal places. Round `p_value_ztest` to 4 decimal places. The `alpha` and `beta` values must be exact integers.

Please complete the task by writing and executing the necessary Python code.