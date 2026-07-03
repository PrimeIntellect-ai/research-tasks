You are a data analyst tasked with building a reproducible pipeline to evaluate an A/B test for a recent marketing campaign. The data is scattered across three CSV files that need to be joined and analyzed. 

The three files are located in `/home/user/data/`:
1. `users.csv`: Contains `user_id` and `region` (e.g., North, South, East, West).
2. `exposures.csv`: Contains `user_id` and `variant` ('Control' or 'Treatment').
3. `purchases.csv`: Contains `purchase_id`, `user_id`, and `amount`.

Your objective is to write a Python script that calculates the 95% bootstrap confidence interval for the difference in mean revenue between the Treatment and Control groups, but ONLY for users in the **'North'** region.

Here are the exact requirements for your analysis:
1. Join the datasets. Keep all users who are in the `exposures.csv` file and belong to the 'North' region in `users.csv`.
2. Calculate the total purchase `amount` for each user. If a user has no purchases in `purchases.csv`, their total amount is 0.
3. Calculate the observed difference in means: `Mean(Treatment) - Mean(Control)`.
4. Perform a bootstrap analysis to find the 95% confidence interval of this difference:
   - Use exactly `10000` bootstrap iterations.
   - Set `numpy.random.seed(42)` immediately before starting your bootstrap loop to ensure reproducibility.
   - For each iteration, sample with replacement from the Control group (size equal to the original Control group size) and independently from the Treatment group (size equal to the original Treatment group size). Calculate the difference in means for the resamples.
   - Use `numpy.percentile` to calculate the 2.5th and 97.5th percentiles of the bootstrapped differences.
5. Create a JSON report at `/home/user/ab_test_results.json` containing the rounded results (to exactly 4 decimal places) using the following keys:
   - `"diff"`: The observed difference in means.
   - `"ci_lower"`: The 2.5th percentile of the bootstrap differences.
   - `"ci_upper"`: The 97.5th percentile of the bootstrap differences.

You may install `pandas` and `numpy` if they are not already installed. Create the script, run it, and ensure the JSON file is generated correctly.