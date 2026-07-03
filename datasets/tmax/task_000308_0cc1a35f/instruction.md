You are a Machine Learning Engineer tasked with preparing training data from raw observational datasets and extracting foundational features using mathematical optimization.

Your goal is to process the raw datasets, perform a curve-fitting optimization, output the results, and write a regression test for your optimization logic.

**Task Steps:**
1. Install `pandas`, `scipy`, and `pytest` using pip.
2. You are provided with two raw data files:
   - `/home/user/raw_data/part1.csv` (columns: `timestamp`, `feature_alpha`)
   - `/home/user/raw_data/part2.csv` (columns: `timestamp`, `feature_beta`)
3. Write a Python script to reshape the data: merge the two files on `timestamp` (inner join) and sort the resulting dataset in ascending order by `timestamp`.
4. Save this merged and sorted dataset to `/home/user/processed_data.csv` (keep the header, do not include the row indices).
5. In a Python module named `/home/user/optimizer.py`, write a function `fit_exponential(df)` that takes the merged DataFrame and uses `scipy.optimize.minimize` or `scipy.optimize.curve_fit` to fit the relationship:
   `feature_beta = A * exp(-B * feature_alpha)`
   Find the optimal parameters `A` and `B` that minimize the mean squared error. Assume `A > 0` and `B > 0`.
6. Call this function on your merged data and save the resulting parameters to `/home/user/params.json` as a JSON object with keys `"A"` and `"B"` and their corresponding float values.
7. Write a regression test in `/home/user/test_optimization.py` using `pytest`. This test should:
   - Import your `fit_exponential` function.
   - Generate a synthetic pandas DataFrame where `feature_alpha` is `[0, 1, 2]` and `feature_beta` is exactly `[2.5 * exp(-0.5 * 0), 2.5 * exp(-0.5 * 1), 2.5 * exp(-0.5 * 2)]`.
   - Assert that the fitted `A` is within `0.01` of `2.5`, and `B` is within `0.01` of `0.5`.
8. Run your test suite using `pytest /home/user/test_optimization.py` to ensure your mathematical optimization is sound.