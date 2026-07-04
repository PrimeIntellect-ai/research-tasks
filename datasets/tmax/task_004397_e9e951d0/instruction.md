You are an AI assistant helping a data researcher fix a broken data processing pipeline. 

The researcher has a bash script located at `/home/user/process.sh`. This script is supposed to read `/home/user/dataset.csv`, perform a simple dimensionality reduction (drop columns with missing data), run a simulated linear model inference using `awk`, and save the output to `/home/user/predictions.csv`. 

Currently, the pipeline has a few issues (similar to a visualization script producing blank plots due to a misconfigured backend):
1. The inference step is outputting invalid or zero values instead of the correct mathematical predictions.
2. The pipeline fails reproducibility tests because its output order changes randomly on every run.

Your task is to:
1. Identify and fix the bugs in `/home/user/process.sh` using only Bash and standard command-line tools (no Python, Perl, etc.).
   - The inference formula should be: `Score = F1 * 0.5 + F2 * 1.2 - F4`.
   - The output `predictions.csv` must be sorted numerically by the ID column (ascending) to ensure reproducibility.
   - The output should contain NO headers, only the data rows in the format `ID,Score`.
2. Run the fixed `/home/user/process.sh`.
3. Verify pipeline reproducibility by computing the SHA256 hash of `/home/user/predictions.csv` and saving just the hash string (the first field of the `sha256sum` output, without the filename) into `/home/user/pipeline_hash.txt`.

The dataset is small and looks like this:
```csv
ID,F1,F2,F3,F4
1,10,20,,5
2,15,22,1,6
3,12,18,,4
```