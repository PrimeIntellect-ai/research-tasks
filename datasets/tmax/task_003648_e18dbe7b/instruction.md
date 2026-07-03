You are an on-call engineer responding to a 3am page. A critical data processing pipeline running on your system has failed. 

The pipeline uses a bash script located at `/home/user/data_pipeline/process_data.sh` to parse and tally numerical values from an input file. Unfortunately, the input file was deleted from the filesystem by an upstream service immediately after it was passed to the pipeline. The bash script crashed intermittently on this dataset, dropping the execution halfway.

Your tasks:
1. The upstream service is still running as a background Python process named `upstream_service.py`. It still holds the deleted file open in memory. Recover the exact contents of this deleted file and save them to `/home/user/recovered_data.csv`.
2. Determine why `process_data.sh` crashed on this specific dataset. The intermittent failure is due to a statistical anomaly in the dataset causing a fatal array index out-of-bounds error in Bash.
3. Fix `/home/user/data_pipeline/process_data.sh` so that it gracefully **ignores** any negative numbers instead of crashing.
4. Run the fixed script against `/home/user/recovered_data.csv` and redirect the standard output to `/home/user/summary_report.txt`.

The automated test suite will verify the contents of `/home/user/summary_report.txt` to ensure the correct values were processed, and it will check that `recovered_data.csv` matches the original deleted data.