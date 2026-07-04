You are tasked with fixing a data processing pipeline. A colleague wrote a pipeline that processes discrete sensor counts, but we've noticed reproducibility issues downstream. We suspect missing values in the CSV are causing the data loading tools to silently cast integer columns to floats, which throws off our downstream strict-integer projection models.

Your task is to process the data from scratch, ensuring exact data types, and apply a pre-calculated dimensionality reduction projection.

Here are the requirements:
1. Read the dataset located at `/home/user/sensor_data.csv`. It contains a `group_id` column and five feature columns representing discrete counts: `F1`, `F2`, `F3`, `F4`, `F5`.
2. Some feature columns contain missing values. You must impute these missing values using the median of each respective column.
3. **Crucial:** The features must be strictly integers. After imputing, cast the feature columns back to integers. (If the median was a float, use standard integer truncation/casting, e.g., dropping the decimal).
4. Apply a 1D projection (dimensionality reduction) to the features. Project each row's `[F1, F2, F3, F4, F5]` vector onto the pre-computed principal axis vector: `W = [0.2, -0.5, 0.4, 0.7, -0.3]`. The projected value for a row should be the dot product of the row's feature vector and `W`.
5. Aggregate the data: compute the mean of the projected 1D value for each `group_id`.
6. Save the aggregated results to `/home/user/group_projection.csv`. 
   - The CSV must have exactly two columns: `group_id` and `mean_projection`.
   - Round `mean_projection` to 4 decimal places.
   - Sort the rows by `group_id` in ascending order.
   - Include the header row.

You may use any programming language (Python, R, bash tools, etc.) to complete this task.