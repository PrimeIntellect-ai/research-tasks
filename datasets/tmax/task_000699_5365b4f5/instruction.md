You are an MLOps engineer maintaining an artifact tracking system. We have a simple data preprocessing pipeline that prepares features for a classification model. 

The pipeline script is located at `/home/user/pipeline.py`. It reads a dataset from `/home/user/data.csv` and a mapping dictionary from `/home/user/mapping.json`. It maps the `category_id` column to new integer values and fills any unmapped categories with `-1`.

However, there is a bug: because some categories are missing from the mapping, `pandas.Series.map` introduces `NaN` values, which silently casts the entire `category_id` column to floats. Even after filling the `NaN`s with `-1`, the column remains a float type (e.g., `1.0`, `-1.0`). When saved to `/home/user/features.csv`, this formatting breaks our downstream artifact hashing system which strictly expects integer string representations.

Your task:
1. Fix the script `/home/user/pipeline.py` so that the `category_id` column is cast back to an integer type (`int64` or `int`) before being saved to `/home/user/features.csv`. The output CSV must not contain `.0` for the `category_id` values.
2. Create a reproducibility test script at `/home/user/test_pipeline.py`. This script must:
   - Import and run the pipeline (e.g., call `run_pipeline()`).
   - Load the generated `/home/user/features.csv` using pandas.
   - Assert that the `dtype` of the loaded `category_id` column is `int64`.
   - Assert that the numerical mean of the `category_id` column is exactly `0.8`.
   - If both assertions pass, write the exact string `REPRODUCIBILITY_PASSED` to `/home/user/test_result.txt`.

Ensure your test script successfully runs and creates the required output file.