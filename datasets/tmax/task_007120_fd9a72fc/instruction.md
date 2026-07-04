You are a data analyst working on a data processing pipeline. Your team has provided you with two datasets and a preliminary Python analysis script, but the pipeline is incomplete, non-deterministic, and currently failing to produce plots correctly. 

Your objective is to build a robust Bash-based data processing pipeline, fix the Python analysis script, and write a reproducibility test.

**Initial Environment:**
- `/home/user/data/dataset_A.csv`: Contains columns `id,feature1,feature2`
- `/home/user/data/dataset_B.csv`: Contains columns `id,feature3,target`
- `/home/user/scripts/analyze.py`: A Python script intended to perform PCA, run a regression model, and generate a correlation plot. 

**Requirements:**

1. **Data Joining (`/home/user/pipeline.sh`):**
   Write a Bash script named `/home/user/pipeline.sh`. It must first join `dataset_A.csv` and `dataset_B.csv` on the `id` column using native Bash tools (like `join`, `awk`, or `sort`). Ensure the CSV headers are handled properly so the output has exactly one header row: `id,feature1,feature2,feature3,target`. 
   Save the joined data to `/home/user/output/joined_data.csv`.

2. **Debugging Analysis (`/home/user/scripts/analyze.py`):**
   The pipeline must execute `/home/user/scripts/analyze.py` passing the joined CSV as the first argument.
   Currently, the script is failing to produce a plot because it is configured for an interactive display backend, which fails in our headless Linux terminal. Modify `analyze.py` so that:
   - It correctly runs in a headless environment.
   - It saves the correlation plot to `/home/user/output/correlation.png` instead of trying to open a GUI window.
   - It is strictly deterministic (reproducible). Currently, the PCA and Regression initializations might have random variance. Fix any missing random seeds (use seed `42` where applicable) so the output metrics are identical on every run.

3. **Metric Extraction:**
   `analyze.py` outputs several metrics to stdout. Your `pipeline.sh` must capture this output, parse it, and generate a JSON file at `/home/user/output/metrics.json`.
   The JSON must be exactly in this format:
   ```json
   {
     "pca_variance": <extracted_float_value>,
     "r2_score": <extracted_float_value>
   }
   ```

4. **Reproducibility Testing (`/home/user/test_reproducibility.sh`):**
   Write a Bash script at `/home/user/test_reproducibility.sh` that tests the determinism of your pipeline.
   The script must:
   - Run `/home/user/pipeline.sh`.
   - Store the SHA256 checksums of `/home/user/output/correlation.png` and `/home/user/output/metrics.json`.
   - Run `/home/user/pipeline.sh` a second time.
   - Compare the new checksums against the stored ones.
   - Exit with code 0 if the checksums match exactly, and exit with code 1 and print an error message if they differ.

Make sure to create the `/home/user/output/` directory in your scripts before trying to write to it. Do not hardcode the metrics into `metrics.json`; they must be dynamically extracted during the pipeline execution.