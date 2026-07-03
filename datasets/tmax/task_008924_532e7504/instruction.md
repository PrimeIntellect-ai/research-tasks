You are an MLOps engineer responsible for evaluating new model experiments and managing their artifacts. 

We have just completed a new model training run. The predictions from the baseline model and the new experimental model have been dumped as raw binary files:
- `/home/user/artifacts/baseline.bin`
- `/home/user/artifacts/experiment.bin`

Each file contains exactly 1,000,000 64-bit floating-point numbers (IEEE 754, little-endian) representing the model's sequential predictions.

Your task is to write a Rust tool to perform numerical accuracy testing and evaluate the new model against the baseline.

Requirements:
1. Initialize a new Rust project named `evaluator` in `/home/user/evaluator`.
2. Write a Rust program that reads both binary files and computes the Mean Squared Error (MSE) between the baseline predictions and the experiment predictions.
3. The program must output the computed MSE formatted to exactly six decimal places to a new file at `/home/user/metrics/mse_report.txt`.
4. After successfully computing the metric, use standard shell commands to archive the raw prediction files to save storage space. Create a gzipped tarball containing `baseline.bin` and `experiment.bin` (just the files, do not preserve the absolute directory structure inside the tarball) and save it to `/home/user/archive/experiment_run.tar.gz`.

Constraints:
- Ensure you create any directories needed for your output files (e.g., `/home/user/metrics` and `/home/user/archive`).
- Use Rust to calculate the MSE. Do not use external tools like Python or `bc` for the calculation. 
- You may use any standard Rust libraries.

Execute your Rust program so that the `mse_report.txt` file is generated, and then create the required archive.