You are acting as a data scientist cleaning a raw log file of search queries. You need to process a dataset using standard Linux command-line tools (Bash, awk, sed, grep, sort, etc.).

Your input file is located at `/home/user/search_logs.txt`. 
Each line in this file contains a timestamp, a user ID, and a raw search query, separated by a pipe character (`|`). The format is:
`YYYY-MM-DD HH:MM:SS | USER_ID | RAW_QUERY`

You need to write a shell command or short Bash script to process this file and generate a CSV report at `/home/user/user_stats.csv`.

Here are the exact processing steps you must implement:
1. **Normalization & Tokenization**: Extract the `RAW_QUERY`. Convert it entirely to lowercase. Replace any character that is not an alphanumeric character (a-z, 0-9) or a space with a space. Collapse any consecutive spaces into a single space, and strip leading/trailing spaces.
2. **Token Counting**: Count the number of tokens (words separated by spaces) in the normalized query. If the normalized query is empty, the token count is 0.
3. **Aggregation**: For each `USER_ID`, calculate:
   - The total number of queries made by the user.
   - The total number of tokens across all their queries.
   - The maximum number of tokens in a single query.
4. **Output formatting**: Write the aggregated results to `/home/user/user_stats.csv`. 
   - The first line must be exactly the header: `user_id,total_queries,total_tokens,max_tokens`
   - The following lines must contain the calculated statistics for each user, formatted as comma-separated values.
   - Sort the data rows (excluding the header) by `total_queries` in descending order. If there is a tie, sort by `user_id` in ascending alphabetical order.

Example input line:
`2023-10-01 10:05:12 | U123 | What is the best, most amazing pizza?!`
Normalized query: `what is the best most amazing pizza`
Tokens: 7

Ensure your final output is exactly at `/home/user/user_stats.csv` with the correct formatting and sorting.