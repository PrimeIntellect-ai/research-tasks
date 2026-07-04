You are an AI assistant helping a data analyst process inference performance benchmark logs.

We have a collection of CSV files containing inference benchmark data. Each CSV has the following columns:
`timestamp`, `model_id`, `latency_ms`, `memory_mb`, `cpu_util`

Your task is to write a Python CLI script at `/home/user/evaluate_benchmarks.py` that classifies a given benchmark CSV as either "stable" (clean) or "unstable" (evil/anomalous). 

The specific data processing steps and the threshold for instability have been handed to us as an image memo. You will find this image at `/app/criteria.png`. 

To process a file, your script must:
1. Accept a single argument: the path to the CSV file.
2. Read the CSV file.
3. Handle missing values, scale the data, and perform dimensionality reduction exactly as described in the image.
4. Compare the resulting performance anomaly scores against the threshold provided in the image.
5. Exit with status code `0` if the file is "stable" (clean).
6. Exit with status code `1` if the file is "unstable" (evil) due to exceeding the threshold.

Requirements:
- Your script should be callable exactly like this: `python /home/user/evaluate_benchmarks.py <path_to_csv>`
- Ensure you use standard pandas and scikit-learn functions for the transformations.
- Any output to stdout/stderr is ignored; only the exit code matters for the final evaluation.