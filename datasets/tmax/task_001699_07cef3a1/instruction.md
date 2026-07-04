You are an MLOps engineer tasked with tracking experiment artifacts and their inference performance. 

You have been given a directory of model artifacts at `/home/user/models/` and a benchmarking script at `/home/user/benchmark.py`. 

Your goal is to build a short, reproducible Python pipeline script at `/home/user/pipeline.py` that processes these artifacts and outputs a consolidated JSON report.

The pipeline script must perform the following:
1. Discover all `.bin` files in `/home/user/models/`.
2. For each model, determine its file size in bytes (representing storage management metrics).
3. Execute the benchmarking script using `python3 /home/user/benchmark.py <absolute_path_to_model>` which outputs a JSON string to stdout containing `latency_ms` and `throughput`.
4. Combine the file size and the benchmark metrics into a single consolidated report.
5. Save the report to `/home/user/artifact_metrics.json`.

The output `/home/user/artifact_metrics.json` must be a valid JSON object where the keys are the **basenames** of the model files (e.g., `model_alpha.bin`), and the values are objects containing exactly three keys: `size_bytes`, `latency_ms`, and `throughput`.

Example of expected output format in `/home/user/artifact_metrics.json`:
```json
{
  "model_alpha.bin": {
    "size_bytes": 2048,
    "latency_ms": 124.5,
    "throughput": 85.2
  },
  "model_beta.bin": {
    "size_bytes": 4096,
    "latency_ms": 230.1,
    "throughput": 43.4
  }
}
```

After writing the script, execute it so that `/home/user/artifact_metrics.json` is generated.