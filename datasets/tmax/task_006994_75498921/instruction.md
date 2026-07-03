You are a Machine Learning Engineer preparing a dataset for a new classification model. You have two raw sensor data streams saved as CSV files:
1. `/home/user/sensor_a.csv` with columns: `ts,f1,f2`
2. `/home/user/sensor_b.csv` with columns: `ts,f3`

Your task is to join these datasets, engineer new features, generate a classification label, and log basic experiment tracking metrics. You may use any language or shell tools you prefer, but standard Linux command-line utilities (like `awk`, `join`, `sort`) or a quick Python script are well-suited for this.

Perform the following steps:
1. **Multi-source joining**: Perform an inner join on the two files using the `ts` (timestamp) column.
2. **Feature Engineering & Numerical Accuracy**: 
   - Compute `error = f1 - f3`.
   - Compute `ratio = error / f2`. 
   - *Important Numerical Constraint*: If `f2` is exactly `0.0`, set `ratio = 0.0` to avoid division-by-zero errors.
3. **Classification Label**: Create a binary label column `y`. If the square of the ratio (`ratio^2`) is strictly greater than `0.1`, set `y = 1`, otherwise set `y = 0`.
4. **Output Dataset**: Save the joined and processed data to `/home/user/dataset_v1.csv`. It must be a comma-separated file including the header: `ts,f1,f2,f3,error,ratio,y`. Format the floating-point numbers `error` and `ratio` to exactly 4 decimal places (e.g., `0.7500`, `-0.3333`). Sort the final output by `ts` in ascending order.
5. **Experiment Tracking**: Calculate the following summary metrics and write them to `/home/user/metrics.txt` in exactly this format:
   ```
   Total_Samples=<number_of_joined_rows>
   Positive_Class_Ratio=<sum_of_y_divided_by_total_samples_to_4_decimal_places>
   Mean_Error=<sum_of_error_divided_by_total_samples_to_4_decimal_places>
   ```

Note: The input files have headers. Make sure your output files also contain headers where specified.