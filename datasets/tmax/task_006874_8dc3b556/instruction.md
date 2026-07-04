I am an MLOps engineer tracking artifacts from our past training experiments. We have a set of hyperparameters and metrics, and I need you to analyze them and test our inference pipeline for reproducibility using standard Linux command-line tools.

Please perform the following steps:

1. **Correlation Analysis**:
   There is a dataset of experiment runs located at `/home/user/experiments/runs.csv`. 
   Using ONLY `awk`, `bc`, and standard coreutils (do NOT write a Python/R/Perl script for this), calculate the Pearson correlation coefficient between the `learning_rate` (column 2) and the `accuracy` (column 3).
   Save the final correlation value, rounded to 3 decimal places (e.g., `0.842` or `-0.123`), to `/home/user/correlation.txt`. Note: The file has a header row that should be ignored.

2. **Analysis Environment Setup**:
   We have a probabilistic modeling tool located at `/home/user/bin/bayes_infer`. This tool uses underlying numerical libraries that exhibit non-deterministic behavior when multi-threading is enabled. 
   Configure your environment by setting the appropriate environment variables to restrict OpenMP (`OMP_NUM_THREADS`) and OpenBLAS (`OPENBLAS_NUM_THREADS`) to exactly `1` thread.

3. **Bayesian Inference & Pipeline Reproducibility Testing**:
   With the environment correctly restricted to single-threading, run the inference tool:
   `/home/user/bin/bayes_infer --data /home/user/experiments/runs.csv > /home/user/inference_out.txt`
   
   To verify pipeline reproducibility, ensure that multiple executions produce the exact same output. 
   Compute the MD5 checksum of `/home/user/inference_out.txt`. Save ONLY the 32-character MD5 hash string (no filenames or extra spaces) into `/home/user/reproducibility_hash.txt`.

Ensure all output files are placed exactly where requested.