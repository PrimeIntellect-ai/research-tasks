You are an MLOps engineer tasked with cleaning and analyzing experiment tracking artifacts to identify the most efficient model that meets our accuracy standards. 

You have been provided with an experiment log file at `/home/user/experiments.jsonl`. Each line in this file is a JSON object containing the results of an inference performance benchmark for a specific model configuration. The keys are: `model_id`, `config_string`, `latency_ms`, and `accuracy`.

Your goal is to build a reproducible pipeline (e.g., a Python script) that performs the following steps:
1. Read the dataset from `/home/user/experiments.jsonl`.
2. **Handle missing values**: Remove any records where `latency_ms` or `accuracy` is missing (`null`).
3. **Handle outliers**: Calculate the 90th percentile of the `latency_ms` across all valid records (use the standard linear interpolation method, e.g., default `numpy.percentile`). Remove any records where `latency_ms` is strictly greater than this 90th percentile threshold.
4. **Filter by performance**: From the remaining non-outlier records, keep only those models that achieved an `accuracy` of 0.90 or higher (`>= 0.90`).
5. **Identify the best model**: Find the model with the lowest `latency_ms` among those that meet the accuracy requirement.
6. **Compute embedding**: For this single best model, calculate a mock "embedding" by computing the SHA-256 hash of its `config_string` (encode the string to UTF-8 before hashing, and use the hex digest).
7. Write the final result to `/home/user/best_model.json` in the following exact JSON format:
```json
{
  "model_id": "<model_id>",
  "embedding": "<sha256_hex_digest>",
  "latency_ms": <latency_ms>
}
```

Write and execute the necessary code to process the data and generate the output file.