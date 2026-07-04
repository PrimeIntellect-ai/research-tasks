You are tasked with building a configuration drift detection system. As a configuration manager, you need to track changes across multiple servers and identify configurations that have diverged too far from each other using mathematical similarity.

Your pipeline must read raw configuration files, clean and normalize them, compute the pairwise Jaccard similarity, log the anomalous pairs, and be scheduled via cron.

**Step 1: Data Cleaning and Normalization**
Write a Python script `/home/user/drift_detector.py` that reads all `.ini` files in `/home/user/configs/raw/`. 
For each file, you must extract a normalized set of configuration pairs:
1. Ignore empty lines and lines starting with `#`.
2. Extract key-value pairs separated by the first `=`. 
3. Lowercase the key, and strip leading/trailing whitespace from both the key and the value.
4. If duplicate keys exist in the same file, keep only the *last* value parsed for that key.
5. Combine them into a normalized string format: `"key=value"`. The configuration of a server is represented by the mathematical set of these normalized strings.

**Step 2: Distance/Similarity Computation**
In the same script, compute the pairwise **Jaccard Similarity** between all unique pairs of configuration files.
* Jaccard Similarity = (Size of Intersection of the two sets) / (Size of Union of the two sets).
* A pair is considered "anomalous" (drifting) if their Jaccard similarity is strictly less than `0.35`.

**Step 3: Output Generation**
The script must create or overwrite a CSV file at `/home/user/reports/anomalies.csv`.
The CSV must contain a header: `file1,file2,similarity`
Write all anomalous pairs to this file. 
* `file1` and `file2` should be the basenames of the files (e.g., `server1.ini`).
* Order the pair such that `file1` comes alphabetically before `file2`.
* Sort the rows in the CSV alphabetically by `file1`, then by `file2`.
* Format the `similarity` score as a float rounded to exactly 4 decimal places (e.g., `0.2500`).

**Step 4: Pipeline Scheduling**
1. Create a bash script `/home/user/run_pipeline.sh` that executes your Python script. Ensure it is executable.
2. Schedule this script to run every minute using the current user's crontab.
3. Run the pipeline manually once so the `anomalies.csv` file is immediately generated for verification.

Directory structure to assume (you must create `/home/user/reports`):
`/home/user/configs/raw/` containing the raw INI files.