You are a Machine Learning Engineer preparing a training dataset. You have been given a raw dataset and a buggy preprocessing pipeline script. Your goal is to fix the script to enforce data schemas, perform correct dimensionality reduction, and compute feature correlations.

The working directory contains:
- `/home/user/data/raw_features.csv`: The raw input data.
- `/home/user/scripts/preprocess.py`: A buggy preprocessing script.

Your tasks:
1. **Schema Enforcement**: The script currently replaces invalid `category` values (`999`) with `NaN`, which silently converts the `category` column from `int64` to `float64`. Fix this by replacing `999` with `-1` and ensuring the final `category` column is strictly of type `int64` in pandas.
2. **Dimensionality Reduction & Numerical Accuracy**: The script implements a manual PCA (Principal Component Analysis) to reduce columns `f1` through `f5` into two components (`pca_1` and `pca_2`). However, it fails to mean-center the features before computing the covariance matrix and projecting the data. Fix the PCA implementation. The mean of `f1` to `f5` must be subtracted before projection.
3. **Pipeline Execution**: The script must save the final dataframe (`id`, `category`, `pca_1`, `pca_2`, `target`) to `/home/user/results/clean_data.csv` (without the index).
4. **Correlation Analysis**: Compute the Pearson correlation coefficient between `pca_1` and `target` in the final cleaned dataset. Save the absolute value of this correlation, rounded to 4 decimal places, to a new file `/home/user/results/abs_corr_pca1_target.txt`.

Ensure your modified `preprocess.py` runs successfully without errors and produces the required output files. 

*Note: You may install standard Python data science libraries like `pandas` and `numpy` if needed.*