You are an AI assistant helping a researcher organize and prepare datasets for a tokenization pipeline. 

The researcher has a script `/home/user/pipeline.py` that reads a dataset (`/home/user/data.csv`), computes token lengths, and outputs a JSON file (`/home/user/output.json`). However, there is a data type issue: because some rows have missing text or missing category IDs, pandas silently converts the `category_id` and `token_length` columns to floats (e.g., `1.0` instead of `1`). 

Your tasks are:

1. **Fix the Pipeline (`/home/user/pipeline.py`)**: 
   Modify the script so that `category_id` and `token_length` are strictly integers (e.g., `1`, not `1.0`) in the output JSON. Missing values for these columns must be represented as JSON `null`. The output JSON file must be saved to `/home/user/output.json`. Ensure the script runs successfully.

2. **Pipeline Reproducibility Testing (`/home/user/test_pipeline.py`)**:
   Create a test script that imports and runs your fixed pipeline, loads the resulting `/home/user/output.json`, and programmatically asserts that no `float` types exist for the `category_id` and `token_length` fields across all records. If a float is found, the script should raise an `AssertionError`.

3. **Inference Performance Benchmarking (`/home/user/benchmark.py`)**:
   Create a benchmarking script that imports `process_data` from `pipeline.py`, runs it 100 times using the `timeit` module, and writes the total execution time (as a plain float string) to `/home/user/benchmark.txt`.

The original `pipeline.py` and `data.csv` have been placed in `/home/user`.