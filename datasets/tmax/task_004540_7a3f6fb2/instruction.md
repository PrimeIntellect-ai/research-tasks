You are a data scientist tasked with building a reproducible data cleaning and modeling pipeline. You have been provided with three noisy CSV datasets in `/home/user/raw_data/` (named `data_0.csv`, `data_1.csv`, and `data_2.csv`). 

Your objective is to build an end-to-end pipeline that handles large-scale data storage, cleans the dataset, trains a regression model, and tracks the experiment reproducibly.

Perform the following tasks:

1. **Data Consolidation and Cleaning (`/home/user/pipeline.py`)**:
    * Write a Python script named `/home/user/pipeline.py`.
    * Load and concatenate the three CSV files from `/home/user/raw_data/`.
    * The dataset has columns `feature_0` through `feature_9` and a `target` column.
    * **Clean the data**: 
        * Drop any rows where the `target` column contains a NaN value.
        * Filter the dataset to only include rows where `feature_0` is strictly between -10.0 and 10.0 (inclusive, i.e., `-10.0 <= feature_0 <= 10.0`).
    * **Storage Management**: Save this cleaned dataset as an HDF5 file at `/home/user/processed_data/clean_data.h5` under the key `dataset`.

2. **Modeling and Experiment Tracking (also in `/home/user/pipeline.py`)**:
    * Using `scikit-learn`, instantiate a `Ridge` regression model with `alpha=1.0` and `random_state=42`.
    * Train the model on the cleaned dataset using `feature_0` through `feature_9` to predict `target`.
    * Calculate the Mean Squared Error (MSE) on the *training* set.
    * Calculate the sum of the learned coefficients.
    * Save these metrics in a JSON file at `/home/user/metrics.json` with the exact keys `"mse"` and `"coef_sum"`. 

3. **Numerical Configuration & Reproducibility (`/home/user/run.sh`)**:
    * To ensure absolute pipeline reproducibility and prevent non-deterministic behavior from multi-threaded numerical libraries, write an executable bash script `/home/user/run.sh`.
    * This script must export the following environment variables:
        * `PYTHONHASHSEED=42`
        * `OMP_NUM_THREADS=1`
        * `OPENBLAS_NUM_THREADS=1`
        * `MKL_NUM_THREADS=1`
    * After exporting the variables, the script must execute `python /home/user/pipeline.py`.

Requirements:
- Ensure you create the `/home/user/processed_data/` directory before saving the HDF5 file.
- Do not use absolute paths that depend on a specific system setup other than `/home/user/`.
- Your final output will be tested by executing `/home/user/run.sh` and validating the contents of `/home/user/processed_data/clean_data.h5` and `/home/user/metrics.json`.