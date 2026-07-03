You are an AI assistant helping a bioinformatics researcher organize their messy datasets. 

The researcher has a dataset directory located at `/home/user/dataset`. It contains various compressed CSV files (`*.csv.gz`) spread across several subdirectories. Unfortunately, an automated tool recently ran amok and created some infinite symlink loops within the directory structure (e.g., directories linking back to their parents). 

Your task is to write and execute a Python script at `/home/user/compile_results.py` that safely traverses this directory, processes the compressed data, and creates a clean, aggregated output file using atomic write operations.

Specifically, your script must:
1. **Metadata-based file search:** Traverse `/home/user/dataset` to find all files ending in `.csv.gz`. You must follow valid directory symlinks to discover files, but you **must detect and avoid infinite symlink loops** (otherwise your script will hang or crash).
2. **Compressed stream processing:** Read the contents of each discovered `.csv.gz` file directly without extracting it to disk. 
3. **Text transformation:** Each CSV file has the following header: `record_id,experiment_name,status,measurement`. 
   - Filter out any rows where the `status` is not exactly `VALID`.
   - For the valid rows, extract the `record_id` and the `measurement` columns.
   - Multiply the `measurement` value by `100.0` (treat as float).
4. **Atomic writes:** Aggregate all valid, transformed rows into a new file. You must write the output to a temporary file first (e.g., `/home/user/clean_dataset.tmp`) and then atomically rename it to the final destination `/home/user/clean_dataset.csv`.
5. **Output Format:** The final `/home/user/clean_dataset.csv` file must have the header `record_id,scaled_measurement`. The subsequent rows must be sorted in ascending numerical order by `record_id`.

Once you have written the script, execute it to produce `/home/user/clean_dataset.csv`.

Ensure your final output file strictly follows the format and sorting rules, as it will be used in downstream pipelines.