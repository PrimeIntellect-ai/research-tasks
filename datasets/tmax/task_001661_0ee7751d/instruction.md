You are an ML Engineer preparing training data for a new pipeline. The previous engineer left behind a raw dataset and some extracted weights for a baseline logistic regression model, but lost the inference script. Your task is to perform feature engineering, reconstruct the baseline model's inference logic to generate baseline predictions, and perform a bootstrap stability analysis on the predictions.

You have been provided with two files:
1. `/home/user/raw_data.csv`: The raw dataset containing columns `id`, `var_a`, `var_b`, `category_c`, and `target`.
2. `/home/user/model_weights.json`: A JSON file containing the weights for a linear combination.

Write and execute a Python script to perform the following steps:

**Step 1: Feature Engineering**
Read `/home/user/raw_data.csv` and create the following features:
- `feature_1`: The product of `var_a` and `var_b`
- `feature_2`: The sum of the squares of `var_a` and `var_b` (i.e., $var\_a^2 + var\_b^2$)
- `category_c_encoded`: The target encoding of `category_c`. For each unique value in `category_c`, calculate the mean of `target` across the entire dataset, and map this mean back to the rows.

**Step 2: Model Architecture Reconstruction & Inference**
Load the weights from `/home/user/model_weights.json` (keys: `intercept`, `w_f1`, `w_f2`, `w_cat`).
Reconstruct the baseline model inference by calculating a linear combination:
$z = intercept + (w\_f1 \times feature\_1) + (w\_f2 \times feature\_2) + (w\_cat \times category\_c\_encoded)$

Then, compute the predicted probability (`baseline_prob`) by applying the sigmoid function:
$baseline\_prob = \frac{1}{1 + e^{-z}}$

**Step 3: Prepare Processed Dataset**
Create a final dataframe containing only the following columns in this exact order:
`id`, `feature_1`, `feature_2`, `category_c_encoded`, `baseline_prob`, `target`.
Round all float columns to exactly 4 decimal places. Sort the dataframe by `id` in ascending order.
Save this dataframe to `/home/user/processed_data.csv` (include the header, do not include the index).

**Step 4: Bootstrap Analysis**
Evaluate the stability of the `baseline_prob` using bootstrap sampling.
- Set the global numpy random seed: `np.random.seed(42)`
- Perform exactly 100 bootstrap iterations. For iteration `i` (from 0 to 99), draw `N` row indices using `np.random.choice(N, size=N, replace=True)` where `N` is the number of rows in the dataset.
- For each bootstrap sample, calculate the mean of the `baseline_prob` column.
- Sort these 100 mean values in ascending order and round them to 4 decimal places.
- Save these sorted means to a file named `/home/user/bootstrap_means.csv` with a single column header `mean_prob` (one value per line).