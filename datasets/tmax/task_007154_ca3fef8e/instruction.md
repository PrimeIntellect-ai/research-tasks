You are a data engineer building an ETL pipeline to process legacy server logs. You need to write a C program and a shell script to clean, transform, and sample the data.

The raw log file is located at `/home/user/data/raw_logs.csv`. It is encoded in `ISO-8859-1` and contains French characters. 
The CSV has the following format (no header):
`id,status_code,response_time_ms,message`

You must create a pipeline consisting of a bash script `/home/user/pipeline.sh` and a C program `/home/user/processor.c`. 

Your C program (`processor.c`) should read from standard input and do the following:
1. **Regex Filtering**: Use POSIX Extended Regular Expressions (`regex.h`) to filter and process ONLY rows where the `message` field contains a pattern matching `ERR-[A-Z]{3}-[0-9]{2}`.
2. **Rolling Aggregation**: For ALL rows that match the regex pattern, maintain a rolling average of the `response_time_ms` for the last 3 matched rows. (For the first matched row, the average is just its response time; for the second, the average of the two, etc. Use integer division for the average to keep it simple).
3. **Stratified Sampling**: We only want a small representative sample. For the rows that matched the regex, output ONLY the first 2 occurrences for each unique `status_code`. You should still update the rolling average even if a row is not printed due to this sampling limit.
4. Output the selected sampled rows to standard output in the following comma-separated format:
`status_code,response_time_ms,rolling_average_ms,message`

Your bash script (`pipeline.sh`) must:
1. Compile the C program (`gcc -O2 processor.c -o processor`).
2. Handle the character encoding transformation: convert the input file from `ISO-8859-1` to `UTF-8`.
3. Pipe the converted data into your compiled C program.
4. Save the standard output of the C program to `/home/user/sampled_metrics.csv`.

Ensure your bash script is executable. You only need to write the code; do not run the pipeline as a background service. Just ensure that running `/home/user/pipeline.sh` completely processes the data and generates `/home/user/sampled_metrics.csv`.