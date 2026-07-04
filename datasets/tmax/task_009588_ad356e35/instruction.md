I am preparing training data for a new machine learning model and need you to build a reproducible ETL pipeline in Bash. 

I have two raw data sources containing different features for our users. 
Source A is located at `/home/user/data/features_a.csv` (columns: `id,f1`).
Source B is located at `/home/user/data/features_b.csv` (columns: `id,f2`).

Please write an executable Bash script at `/home/user/prepare_data.sh` that performs the following steps:
1. Joins the two datasets on the `id` column.
2. Reconstructs a baseline target variable `y` using the following mathematical model: `y = (f1^2) + (3 * f2) - 14`.
3. Filters the dataset to retain only the records where `y` is strictly greater than 0.
4. Saves the resulting data to `/home/user/data/training_set.csv` with the exact header `id,f1,f2,y`.
5. The rows in `training_set.csv` (excluding the header) must be sorted numerically by `y` in descending order. If there is a tie in `y`, sort by `id` in ascending order.

Ensure your script handles the CSV headers correctly during the join and calculation steps. You can use any standard Linux text processing utilities (like `awk`, `join`, `sort`, etc.) available in bash. Run your script to generate the final `training_set.csv` file so I can verify the results.