You are an MLOps engineer tasked with investigating a potential data leak in a machine learning experiment. It appears that some samples might have leaked between the training and test sets during the pipeline execution. You need to identify these leaked samples, join their features from multiple upstream sources to inspect them, and benchmark the inference performance on this subset.

Write a reproducible bash script at `/home/user/investigate_leak.sh` that performs the following steps when executed:

1. **Find Leaked IDs**:
   - You are provided with two artifact files: `/home/user/data/train.csv` and `/home/user/data/test.csv`. Both files have headers, and the first column is `id`.
   - Identify the `id`s that are present in BOTH `train.csv` and `test.csv`.
   - Save these leaked `id`s (excluding the header 'id') in sorted numerical order to `/home/user/leaked_ids.txt`, with one ID per line.

2. **Multi-source Data Joining**:
   - The original raw features come from two separate files: `/home/user/data/source_A.csv` (columns: `id,featA`) and `/home/user/data/source_B.csv` (columns: `id,featB`).
   - For ONLY the leaked IDs identified in Step 1, join `source_A.csv` and `source_B.csv` on the `id` column.
   - Save the result to `/home/user/leaked_features.csv`. The output format must be comma-separated, without headers, in the format: `id,featA,featB`. The rows must be sorted by `id` numerically.

3. **Inference Performance Benchmarking**:
   - You are provided with an inference script at `/home/user/inference_batch.py` which takes a file of IDs as a positional argument.
   - Run the python script on your `/home/user/leaked_ids.txt` file.
   - You must benchmark the runtime of this script using the `time -p` bash command.
   - Save the standard output of the python script to `/home/user/leak_predictions.txt`.
   - Save the output of the `time -p` command (which prints `real`, `user`, and `sys` times) to `/home/user/benchmark.txt`.

Ensure your bash script is executable. You do not need to run the script yourself, but the automated test will execute `/home/user/investigate_leak.sh` to verify your solution.