I need your help building a robust data processing pipeline in Bash to clean up a messy ETL process. We have a daily raw dataset of events, and we use a proprietary, compiled tool to extract features from it. However, the tool is buggy: when it runs, it often spits out duplicate records and outputs rows out of order. 

Your objective is to write a Bash script `/home/user/pipeline.sh` that processes the data, cleans it, applies a rolling aggregation, and prepares a stratified sample.

Here are the requirements:
1. **Input Data**: You will process `/home/user/events.csv`, which has a header `id,timestamp,category,raw_value`.
2. **Feature Extraction**: Pipe the raw data (including the header) through the proprietary binary `/app/feature_extractor`. This tool reads CSV from stdin and outputs CSV to stdout with the format `id,timestamp,category,extracted_value`. 
3. **Deduplication & Sorting**: The binary injects duplicate `id`s and shuffles the rows. You must deduplicate the output so that each `id` appears exactly once, and then sort the dataset chronologically by `timestamp` (oldest first).
4. **Rolling Aggregation**: Using standard Linux tools (like `awk`), compute a rolling average of the `extracted_value`. The rolling window should be size 3 (the current record and the up to 2 preceding records). 
5. **Stratified Sampling**: We only want a subset of the data for downstream bulk import into our database. Extract exactly the first 2 chronological records for each unique `category`.
6. **Output**: Write the final dataset to `/home/user/final_sample.csv` with the header `id,timestamp,category,extracted_value,rolling_avg`. The `rolling_avg` should be formatted to 2 decimal places.

Make sure your script is executable. I will run `/home/user/pipeline.sh` to generate the output file. The automated grading will compute the Mean Absolute Error (MAE) of your `rolling_avg` column against our reference implementation.