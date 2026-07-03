You are helping a researcher who is organizing datasets collected from various sensor deployments. The researcher has a baseline "clean" dataset and several new data batches. They suspect some batches might be experiencing sensor drift (corruption) and need you to verify them using an existing machine learning model and statistical tests.

Here is your task:

1. **Reconstruct the Model:**
   The researcher trained a simple PyTorch model, but lost the original code. You need to reconstruct it. The model is a Multi-Layer Perceptron (MLP) for regression with the following architecture:
   - Input layer: 4 features
   - Hidden layer: 16 units with a ReLU activation function
   - Output layer: 1 unit (no activation function)
   The saved state dictionary is located at `/home/user/model/weights.pth`.

2. **Run Inference & Numerical Accuracy Testing:**
   The datasets are located in `/home/user/data/`. They are CSV files with no header. The first 4 columns are the features, and the 5th column is the true target value.
   - `clean.csv`
   - `batch_1.csv`
   - `batch_2.csv`
   - `batch_3.csv`
   Load the weights into your reconstructed model. Run inference (in evaluation mode) on all datasets and calculate the Mean Squared Error (MSE) for each.

3. **Identify Corrupted Batches & Hypothesis Testing:**
   A batch is considered "corrupted" if its MSE is strictly greater than `2.0`.
   For every corrupted batch, perform Welch's t-test (two-sided, unequal variances) to compare the mean of the model's **predicted values** for that batch against the mean of the model's **predicted values** for the `clean.csv` dataset.
   Additionally, calculate the 95% Confidence Interval for the difference in means (Corrupted Predicted Mean - Clean Predicted Mean). Use the standard normal approximation (z=1.96) or t-distribution for the CI calculation.

4. **Reporting:**
   Generate a JSON report at `/home/user/results.json` with the following exact structure:
   ```json
   {
       "mse": {
           "clean": <float>,
           "batch_1": <float>,
           "batch_2": <float>,
           "batch_3": <float>
       },
       "corrupted_batches": {
           "batch_X": {
               "t_statistic": <float>,
               "p_value": <float>,
               "ci_lower": <float>,
               "ci_upper": <float>
           }
       }
   }
   ```
   (Only include the actually corrupted batches in the `corrupted_batches` dictionary).

Ensure your output matches the JSON structure perfectly. Round all floating-point numbers in the final JSON to 4 decimal places.