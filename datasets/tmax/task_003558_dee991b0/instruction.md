You are acting as a localization engineer managing a continuous translation pipeline. You have a raw event log containing translation updates over time, but it contains duplicate submissions for the same text strings and is difficult to analyze. 

Your task is to build a multi-stage data processing pipeline using Bash and a custom C program to deduplicate the events, bucket them by day, and calculate the daily translation velocity (word count) per language.

**Input Data:**
A log file at `/home/user/loc_events.log`. 
It is a comma-separated file where each line has the following format:
`UNIX_TIMESTAMP,STRING_MD5_HASH,LANGUAGE_CODE,WORD_COUNT`
*(The file is already chronologically sorted by timestamp).*

Example:
```
1696118400,a8f5f167f44f4964e6c998dee827110c,es-ES,14
1696120500,b9g5f167f44f4964e6c998dee827110a,fr-FR,8
1696122000,a8f5f167f44f4964e6c998dee827110c,es-ES,14
```
*(Notice the third line is a duplicate submission of the first line's hash).*

**Requirements:**
1. **C Program (`/home/user/aggregate.c`):** Write a C program that reads the CSV data from standard input.
    * **Hash-based Deduplication:** It must track the `STRING_MD5_HASH` values it has seen. If a hash has already been processed in the stream, ignore the line completely. (You can assume a maximum of 50,000 unique hashes. POSIX `search.h` or a simple custom hash table is recommended).
    * **Time-based Bucketing & Aggregation:** For each unique translation event, convert the `UNIX_TIMESTAMP` to a UTC date string in the format `YYYY-MM-DD`. Aggregate the total `WORD_COUNT` for each `YYYY-MM-DD` and `LANGUAGE_CODE` combination.
    * **Output:** Print the aggregated results to standard output in the format: `YYYY-MM-DD,LANGUAGE_CODE,TOTAL_WORDS`

2. **Pipeline Script (`/home/user/pipeline.sh`):** Write a Bash script that:
    * Compiles your C program using `gcc` (with standard optimizations like `-O2`).
    * Pipes `/home/user/loc_events.log` into the compiled C executable.
    * Pipes the output of the C program into a standard bash `sort` command to sort the results chronologically by date (first column) and then alphabetically by language code (second column).
    * Saves the final, sorted output to `/home/user/daily_velocity.csv`.

**Acceptance Criteria:**
- The Bash script must be executable and runnable without arguments.
- The final output `/home/user/daily_velocity.csv` must precisely match the format `YYYY-MM-DD,LANGUAGE_CODE,TOTAL_WORDS`.
- Duplicates of any string hash must not contribute to the daily word count. Only the *first* chronological occurrence of a hash counts.