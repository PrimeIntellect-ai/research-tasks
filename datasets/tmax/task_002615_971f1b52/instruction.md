We are migrating our legacy ETL pipelines to a more maintainable shell-based architecture. A critical part of our real-time streaming pipeline is currently handled by an undocumented, compiled C binary located at `/app/legacy_etl`. 

We need you to reverse-engineer its behavior (or simply replace it based on the specs below) and write a pure Bash/standard Unix utility script that perfectly replicates its output. 

Here is what we know about the stream processing pipeline:
1. It reads raw data from `stdin` and writes the processed data to `stdout`.
2. The input data is a large CSV stream without headers. Each line has exactly 4 columns: `id,category,value,notes`.
3. The `notes` column is currently encoded in `ISO-8859-1` (Latin-1).
4. **Data Sampling:** The pipeline implements a stratified sampling rule. It ONLY outputs rows where the `id` (an integer) is exactly divisible by `10`. All other rows are dropped.
5. **Interpolation/Imputation:** The `value` column (a float) is sometimes missing (empty). When it is missing, the pipeline imputes it with the string `0.0`.
6. **Character Encoding Handling:** The pipeline converts the entire output to `UTF-8` so downstream systems can read the `notes` column properly. 
7. The output must be a valid CSV matching the transformed data: `id,category,value,notes`.

Your tasks:
1. Analyze `/app/legacy_etl` if needed, but your goal is to write a replacement script at `/home/user/process_stream.sh`.
2. `/home/user/process_stream.sh` must accept input on `stdin`, stream the processing efficiently (do not load the whole file into memory), and print to `stdout`. It must be bit-for-bit identical to the legacy binary's output for any valid input stream.
3. Make the script executable.
4. **Pipeline scheduling:** We need to run a batch job every night. Set up a cron job for the `user` that runs `/home/user/process_stream.sh < /data/daily.csv > /data/processed.csv` exactly at 02:30 AM every day.

Ensure your bash script handles the stream efficiently using standard Linux text-processing tools (e.g., `awk`, `iconv`, `sed`).