You are an AI assistant helping a data science researcher build a reproducible data processing pipeline. The researcher is organizing multi-source datasets and needs a robust script to join data, validate model outputs against thresholds, and track experiments using a local database.

The researcher uses a specific vendored version of `tinydb` for experiment tracking because of compliance requirements, but it's currently broken on this machine.

Your objectives:
1. **Fix the Vendored Package:**
   There is a vendored source of `tinydb` located at `/app/tinydb-4.8.0`. The researcher recently applied a patch that accidentally introduced a bug preventing it from being imported properly (it throws an import error related to `json`). Identify the bug in the vendored source, fix it, and install it into your python environment (e.g., `pip install -e /app/tinydb-4.8.0`).

2. **Write the Pipeline Script:**
   Create a Python script at `/home/user/pipeline.py`. The script must take exactly two arguments:
   `python /home/user/pipeline.py <sensors_csv_path> <predictions_csv_path>`

   *   **Multi-source joining:** Read both CSV files. Both files have an `id` column. Join the datasets on `id` (inner join).
   *   **Model output validation:** The `sensors_csv` contains an `actual_value` column (float). The `predictions_csv` contains a `pred_value` (float) and a `threshold` (float) column. Filter the joined dataset to keep ONLY rows where the absolute difference between `actual_value` and `pred_value` is strictly less than `threshold`.
   *   **Experiment tracking:** Use the fixed `tinydb` library to log the experiment run. Insert a document into a TinyDB database located at `/home/user/experiments.json` with the format: `{"sensors_file": "<sensors_csv_path>", "predictions_file": "<predictions_csv_path>", "valid_count": <number_of_rows_passed_validation>}`.
   *   **Reproducibility/Output:** To allow automated reproducibility testing, your script must print the final filtered, joined dataset to standard output (STDOUT) in standard CSV format, including the header. The header must be exactly `id,actual_value,pred_value,threshold`. The rows must be sorted by `id` in ascending numerical order. Do not print anything else to STDOUT.

Please ensure your script perfectly conforms to these logical requirements, as it will be rigorously tested against hundreds of random dataset pairs.