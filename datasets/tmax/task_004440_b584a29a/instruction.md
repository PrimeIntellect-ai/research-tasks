You are tasked with building a configuration drift analysis pipeline. We have a set of daily server configuration snapshots stored as JSON-Lines files in `/home/user/data/configs/`. Unfortunately, a bug in the configuration collection agent caused some string values to contain malformed Unicode escape sequences (e.g., `\uZZZZ`, `\uXXXX`). Standard JSON parsers fail when reading these files.

Your goal is to write a Python script (e.g., at `/home/user/process_configs.py`) that performs the following steps:

1. **Parallel Data Cleaning & Parsing**: Read and parse all `.jsonl` files in `/home/user/data/configs/`. You must use Python's `concurrent.futures` or `multiprocessing` to process the files in parallel. Before parsing each line, sanitize the JSON string by completely removing any malformed unicode escape sequences that start with `\u` followed by exactly 4 non-hexadecimal characters (or any sequence that would cause a standard JSON parser to throw an error due to invalid hex escapes). 
2. **Similarity Computation**: Each parsed JSON object contains `server_id`, `date` (YYYY-MM-DD), and `packages` (a list of installed package names). For each server, sort the records chronologically. For every day, compute the **Jaccard similarity** between that day's `packages` list and the previous day's `packages` list. 
   - Jaccard similarity is defined as the size of the intersection divided by the size of the union of the two sets.
   - For the very first day a server appears, its similarity score is exactly `1.0`.
3. **Windowed Aggregation**: For each server, compute a **3-day rolling average** of the daily Jaccard similarity scores. 
   - On day 1, the average is just day 1's score.
   - On day 2, the average is the mean of day 1 and day 2's scores.
   - On day 3 and beyond, the average is the mean of the scores from day $T$, day $T-1$, and day $T-2$.
4. **Join & Identify**: Find the minimum 3-day rolling average score across all days for each server. Join this data with `/home/user/data/metadata.csv` (which contains `server_id` and `owner_email`) to find the email address of the owner of the server that experienced the most drift (i.e., the server with the **lowest** minimum 3-day rolling average score).
5. **Output**: Write the result to `/home/user/report.json` in the exact following format, rounding the score to 4 decimal places:
```json
{
  "most_drifted_server": "<server_id>",
  "owner_email": "<email>",
  "min_rolling_score": 0.1234
}
```

Constraints:
- You must use Python. Standard library is sufficient, but `pandas` is permitted if installed.
- Ensure your script completes successfully and creates the `/home/user/report.json` file.