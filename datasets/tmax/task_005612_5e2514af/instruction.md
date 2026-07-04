You are a data analyst tasked with processing a dataset of numerical features and validating a pre-computed linear model's outputs. 

You need to write a Go program that performs linear projection (feature engineering), validates the predictions against ground truth targets, and flags anomalies.

Here are your instructions:
1. Two files have been provided for you:
   - `/home/user/input.csv`: Contains the dataset. The header is `id,v1,v2,v3,target`.
   - `/home/user/weights.csv`: Contains a single row of 3 weights (comma-separated, no header) corresponding to `v1, v2, v3`.
2. Write a Go program (save it at `/home/user/evaluate.go`) that reads both files.
3. For each row in `input.csv`, compute the predicted value `y_pred` as the dot product of the feature vector `[v1, v2, v3]` and the weights vector.
4. Calculate the Mean Squared Error (MSE) across all rows between `y_pred` and the `target` column.
5. Identify any "anomalous" rows where the absolute error `|y_pred - target|` is strictly greater than `2.0`.
6. Write the results to a log file exactly at `/home/user/validation.txt` with the following format:
   - The first line must be exactly `MSE: <value>`, where `<value>` is the MSE formatted to exactly 4 decimal places.
   - The second line must be exactly `Anomalies:`
   - Each subsequent line must contain the `id` (as an integer) of an anomalous row, listed in the order they appeared in the CSV.

Run your Go program to generate the `/home/user/validation.txt` file. Make sure you use Go to solve this task.