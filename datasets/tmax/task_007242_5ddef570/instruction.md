You are assisting a researcher who is organizing and analyzing a high-dimensional dataset. The dataset has some missing values that caused pandas to silently convert an integer category column into floats.

The researcher wants to assess the stability of the primary axis of variation in this data using bootstrapping, but requires you to clean the data and set up the pipeline.

The dataset is located at `/home/user/dataset.csv`. It contains 50 features named `f1` through `f50`.

Please write a Python script at `/home/user/analyze.py` that performs the following steps:
1. Ensure the necessary packages are installed (you may need to install `pandas`, `scikit-learn`, and `numpy` in your environment first).
2. Load `/home/user/dataset.csv`.
3. The feature `f1` was originally meant to be an integer type but contains `NaN` values. Fill all `NaN` values in `f1` with the median of the non-missing values in `f1`, and then explicitly cast the entire `f1` column to an integer type.
4. Perform a bootstrap analysis to find the 95% confidence interval of the explained variance ratio of the *first* principal component (PC1). 
   - Perform exactly 1000 bootstrap iterations.
   - For reproducibility, in your loop use `i` from `0` to `999` as the random state for sampling. Specifically, use `df.sample(frac=1, replace=True, random_state=i)` to generate the bootstrap sample for iteration `i`.
   - On each bootstrap sample, fit a standard PCA (from `sklearn.decomposition`) using all 50 features (`f1` to `f50`).
   - Extract the explained variance ratio of the first principal component and store it.
5. After 1000 iterations, calculate the 2.5th and 97.5th percentiles of the collected PC1 explained variance ratios using `numpy.percentile`.
6. Write these two values, comma-separated and rounded to exactly 4 decimal places, to a file named `/home/user/pca_ci.txt` (e.g., `0.1234,0.1567`).

Execute your script to ensure the output file is generated correctly.