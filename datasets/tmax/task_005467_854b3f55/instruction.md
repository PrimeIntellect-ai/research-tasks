You are a data scientist cleaning up an inference performance benchmark dataset. 

You have been provided with a CSV file at `/home/user/benchmarks.csv`. This file contains three columns: `model_id`, `inference_ms` (inference time in milliseconds), and `confidence_score` (a model output probability metric).

Unfortunately, the logging system had a few bugs, and some rows contain invalid `inference_ms` values (e.g., negative times or non-numeric strings).

Your task:
1. Read `/home/user/benchmarks.csv` and ignore the header row.
2. Filter out any rows where `inference_ms` is not a valid non-negative number (i.e., remove rows where `inference_ms` is less than 0 or contains non-numeric characters).
3. Using only standard Linux command-line tools (like `awk`, `sed`, `grep`, `bc`, etc.), calculate the Pearson correlation coefficient between the valid `inference_ms` values and the `confidence_score` values. Do NOT use Python, R, or any other higher-level scripting languages.
4. Round the final correlation coefficient to 3 decimal places (e.g., `-0.123` or `0.850`) and save it to exactly `/home/user/correlation.txt`. The file should contain only this number and nothing else.