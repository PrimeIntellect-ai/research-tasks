You are an MLOps engineer tasked with consolidating experiment artifacts scattered across different systems into a clean, queryable dataset. 

You have three raw data sources located in `/home/user/`:
1. `experiments.jsonl`: Contains hyperparameter configurations. Each line is a JSON object with `experiment_id`, `learning_rate`, and `batch_size`.
2. `metrics.csv`: Contains the final training metrics. Columns are `experiment_id`, `final_loss`, and `final_accuracy`.
3. `logs.txt`: Contains raw text logs from the training runs. Each line follows the format `[exp_id: <experiment_id>] <log_message>`.

Your task is to build a Python ETL script `/home/user/etl_pipeline.py` that performs the following steps:

**1. Numerical Library Configuration:**
Ensure your script executes efficiently by setting the environment variable `OMP_NUM_THREADS=1` *within* the Python script before importing pandas or numpy.

**2. Tokenization and Data Extraction (Logs):**
Parse `logs.txt`. For each line, extract the `experiment_id`. Take the `<log_message>` portion, convert it to lowercase, and tokenize it by extracting purely alphabetical words (using the regex `\b[a-z]+\b`). 
Count the total number of "error" and "warning" tokens for each `experiment_id`.
*Note: Some experiments may have multiple log lines; aggregate the counts per experiment.*

**3. Multi-source Data Joining:**
Join the parsed logs data (total error count, total warning count), the metrics data, and the configuration data on `experiment_id`. Keep only the experiments that are present in all three data sources (Inner Join).

**4. Feature Engineering:**
Calculate a custom stability score for each joined experiment using the following formula:
`stability_score = final_accuracy / (final_loss + 1e-5) - (0.1 * error_count) - (0.05 * warning_count)`

**5. Output Generation:**
- Save the fully joined dataframe to `/home/user/consolidated_artifacts.parquet` using the Snappy compression engine. (You may need to install `pyarrow` or `fastparquet`).
- Identify the top 3 experiments with the highest `stability_score`. Save their `experiment_id`s to `/home/user/top_experiments.txt`, with one ID per line, sorted in descending order of their score.

Run your ETL script to generate the final outputs.