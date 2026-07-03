You are an MLOps engineer tasked with tracking and analyzing experiment artifacts using only Bash and standard Linux command-line utilities (like `jq`, `awk`, `grep`, `sort`, etc.). No Python scripts are allowed.

You have a directory of JSON files representing model training runs located at `/home/user/experiments/`. Each JSON file is supposed to contain metadata about the experiment.

Your objective is to write a Bash script (or a series of Bash commands) that performs three main tasks: Schema Enforcement, Similarity Search, and Pipeline Reproducibility Testing.

1. **Schema Enforcement**:
   Check all JSON files in `/home/user/experiments/` (excluding `exp_ref.json`). A valid experiment file MUST contain all of the following top-level keys: `experiment_id`, `learning_rate`, `batch_size`, `schema_hash`, `model_weights_hash`, and `accuracy`.
   Identify any files that are missing one or more of these keys.
   Write the base filenames (e.g., `exp_003.json`) of the invalid files, one per line, sorted alphabetically, to `/home/user/report/invalid.log`.

2. **Similarity Search**:
   There is a reference experiment file at `/home/user/experiments/exp_ref.json` (assume it has a valid schema). You need to find the most similar *valid* experiment in the directory.
   Similarity is defined by the minimum Euclidean distance between the hyperparameters `learning_rate` and `batch_size`. 
   Formula: `Distance = sqrt((lr1 - lr2)^2 + (bs1 - bs2)^2)`. Calculate this using the raw values (do not normalize). 
   Write the base filename of the closest matching valid experiment to `/home/user/report/closest.log`.

3. **Pipeline Reproducibility Testing**:
   Among all *valid* experiments (excluding `exp_ref.json`), find pairs of experiments that indicate a reproducibility violation. A violation occurs when two experiments have the exact same `learning_rate`, `batch_size`, and `schema_hash`, but produce a different `model_weights_hash`.
   Write these pairs to `/home/user/report/violations.log`. Each line should represent one violating pair, formatted as `file1.json,file2.json`. The filenames in each pair must be sorted alphabetically (e.g., `exp_001.json,exp_004.json`), and the lines in the file must also be sorted alphabetically.

Ensure the `/home/user/report/` directory is created if it doesn't exist. Produce exactly the three `.log` files specified above.