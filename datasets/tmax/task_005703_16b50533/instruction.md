You are a data analyst optimizing a data processing pipeline. You have been given a set of partitioned CSV files containing user activity data. 

Your objective is to build a multi-stage pipeline that deduplicates records by `user_id` and then performs stratified sampling to extract a fixed number of users per role. Because the dataset is expected to grow, the deduplication must be handled by a highly efficient C program using hash-based deduplication, while the orchestration and sampling can be handled by shell utilities.

Here are your instructions:

1. **The Data**: 
   There are three header-less CSV files located in `/home/user/raw_data/`:
   - `data_1.csv`
   - `data_2.csv`
   - `data_3.csv`
   Each row has the format: `user_id,role,activity_score` (e.g., `u123,admin,85`).

2. **The C Deduplicator**:
   Write a C program at `/home/user/dedup.c` that reads lines from standard input. 
   - It should parse out the `user_id` (the substring before the first comma).
   - It must use the POSIX `<search.h>` library (`hcreate`, `hsearch`, etc.) to keep track of seen `user_id`s. (You can assume a maximum of 10,000 unique keys, so initialize the hash table accordingly).
   - If a `user_id` has NOT been seen before, print the entire unmodified line to standard output. If it has been seen, skip it.
   - Compile this program to `/home/user/dedup` (using `gcc /home/user/dedup.c -o /home/user/dedup`).

3. **The Pipeline Orchestration**:
   Write a bash script at `/home/user/pipeline.sh` that constructs a multi-stage pipeline to do the following:
   - Concatenate the files in exactly this order: `data_1.csv`, `data_2.csv`, `data_3.csv`.
   - Pipe the data stream into your `/home/user/dedup` executable.
   - Pipe the deduplicated output into an `awk` command that performs stratified sampling: for each `role`, keep only the **first 2** records encountered.
   - Redirect the final output to `/home/user/sampled.csv`.

4. Make sure `/home/user/pipeline.sh` is executable and run it so that `/home/user/sampled.csv` is generated.