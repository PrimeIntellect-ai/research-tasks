You are an MLOps engineer responsible for maintaining an automated experiment tracking pipeline. Currently, the pipeline is failing due to two issues: a misconfigured artifact plotting script producing blank or missing plots, and an incomplete Bash benchmarking script.

In `/home/user/mlops_pipeline/`, you will find:
1. `generate_embeddings.py`: A script that simulates inference for a classification model, generates high-dimensional embedding vectors for similarity search, and prints the inference latency to stdout. It accepts a `--batch_size` argument.
2. `plot_artifacts.py`: A dimensionality reduction script (using PCA) that is supposed to read an `embeddings.csv` file and generate a plot `artifact_plot.png`. However, it crashes or produces no plot because of a matplotlib misconfiguration in a headless Linux environment.

Your tasks are:
1. **Fix the plotting script**: Modify `/home/user/mlops_pipeline/plot_artifacts.py` so that it successfully saves a valid (non-empty) PNG file to `/home/user/mlops_pipeline/artifact_plot.png`. Do not change the data processing logic, just fix the matplotlib backend/saving configuration.
2. **Write the benchmarking Bash script**: Create a Bash script at `/home/user/mlops_pipeline/run_experiments.sh`. This script must:
   - Create a `logs` directory in `/home/user/mlops_pipeline/`.
   - Iterate through batch sizes `1`, `2`, `4`, `8`, and `16`.
   - For each batch size, run `python3 generate_embeddings.py --batch_size <size>` and redirect the stdout to `/home/user/mlops_pipeline/logs/run_<size>.log`.
   - Parse the `Latency: <X> ms` line from each log file and create a CSV file at `/home/user/mlops_pipeline/latency_summary.csv` with the exact header `batch_size,latency_ms`, followed by the extracted data sorted by batch size numerically.
   - Run `python3 plot_artifacts.py` at the end of the script to generate the fixed plot.

Ensure your Bash script is executable and run it to produce the final `latency_summary.csv` and `artifact_plot.png`.