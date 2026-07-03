A junior data analyst recently processed our machine learning dataset, but they made a critical error: they introduced data leakage. They normalized a feature using the minimum and maximum values of the *entire* dataset, which leaked information from the test set into the test features.

Your task is to fix this by correctly normalizing the test set using only the statistics derived from the training set.

You are provided with a CSV file at `/home/user/dataset.csv`.
The file has the following schema:
`id,feature_A,feature_B,target,split`

The `split` column contains either `train` or `test`.

Do the following:
1. Identify the minimum and maximum values of `feature_B` (the 3rd column) using **only** the rows where `split` is `train`.
2. Apply Min-Max scaling to `feature_B` for the rows where `split` is `test`, using the minimum and maximum values calculated from the training set.
   The formula is: `scaled_feature_B = (feature_B - train_min) / (train_max - train_min)`
3. Save the results for the test set into a new file at `/home/user/test_scaled.csv`.
4. The output file must enforce the following schema strictly:
   - A header row: `id,scaled_feature_B`
   - Only include rows belonging to the `test` split.
   - The `scaled_feature_B` values must be rounded to exactly 4 decimal places (e.g., `1.8333`, `-0.1667`).

You may use any language or shell CLI tool to accomplish this, but the final output must strictly match the specifications.