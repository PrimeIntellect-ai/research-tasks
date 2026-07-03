You are a data analyst tasked with processing user search logs. For performance reasons, the core feature extraction must be written in C, while the rest of the pipeline can use standard Bash utilities. 

You have two datasets located in your home directory:
1. `/home/user/users.csv`: Contains user demographics (Format: `user_id,age,country`)
2. `/home/user/queries.csv`: Contains search logs (Format: `user_id,query_text`)

Your objectives are:

1. **Feature Engineering & Tokenization (C Programming):**
   Write a C program at `/home/user/processor.c` that:
   - Reads `queries.csv` from standard input.
   - Ignores the header row (`user_id,query_text`).
   - Tokenizes the `query_text` field using the space character (` `) as the delimiter.
   - For each line, calculates:
     - `num_tokens`: The total number of words in the query.
     - `max_token_length`: The length of the longest word in the query.
   - Prints the result to standard output in the format: `user_id,num_tokens,max_token_length` (no header).
   - Compile this program to `/home/user/processor`.

2. **Data Processing (Bash/Coreutils):**
   - Run your compiled `./processor` on `/home/user/queries.csv` and save the output to `/home/user/features.csv`.
   - Join `/home/user/features.csv` with `/home/user/users.csv` based on `user_id`. Note: You must skip the header of `users.csv` before joining, and you may need to sort the files. 
   - The joined output should be formatted as: `user_id,age,country,num_tokens,max_token_length` (comma-separated, no header).
   - Save the joined output to `/home/user/joined_features.csv`.

3. **Sampling & Filtering:**
   - Filter `/home/user/joined_features.csv` to keep only the users who are exactly 30 years old or older (`age >= 30`).
   - Save this filtered dataset to `/home/user/final_sample.csv`.

4. **Experiment Tracking:**
   - Create a log file at `/home/user/experiment_log.txt`.
   - Write exactly one line to this log file containing the number of rows in your final sample, in this exact format: `FINAL_ROWS: <number>`

Make sure your C program handles standard UNIX line endings and gracefully processes the provided CSV structure.