You are an MLOps engineer tasked with fixing an unstable artifact generation pipeline. 

There is a pipeline script located at `/home/user/mlops_pipeline/build_features.py` that processes a raw dataset (`/home/user/mlops_pipeline/raw_data.csv`). The script currently performs TF-IDF tokenization followed by dimensionality reduction using `TruncatedSVD`, and writes the output to `/home/user/mlops_pipeline/artifacts/features.csv`.

However, the downstream artifact tracking system is rejecting the output due to two critical issues:
1. **Type Contamination**: The `author_id` column contains missing values in the raw dataset. Pandas silently reads this column as floating-point numbers (e.g., `10.0`, `NaN`), which breaks downstream systems that strictly expect integers. 
2. **Non-Reproducibility**: The dimensionality reduction step yields slightly different coordinate values on every run because the random seed is not fixed.

Your task is to fix the script `/home/user/mlops_pipeline/build_features.py` so that:
1. Any missing values in the `author_id` column are imputed with the integer `-1`.
2. The entire `author_id` column is cast to standard integers (so they output as `10`, `-1`, `20`, etc. in the CSV, without decimals).
3. The `TruncatedSVD` model is explicitly initialized with `random_state=42` to guarantee reproducible artifact generation.
4. Execute the pipeline so the corrected artifact is written to `/home/user/mlops_pipeline/artifacts/features.csv`.

Do not change the names of the files or the number of SVD components (it should remain 2). When you have successfully run the corrected pipeline, you are finished.