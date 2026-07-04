You are a localization engineer trying to consolidate translation logs from two legacy microservices. You must write a C program that reads a CSV file and a JSON-Lines file, parses their specific timestamp formats, aligns them, decodes Unicode escape sequences, computes the byte-level Levenshtein distance between their source text fields, and outputs the joined results.

The two input files are located at:
1. `/home/user/service_a.csv`
   Format: `timestamp,loc_key,source_text`
   Timestamp format: `YYYY:MM:DD-HH:MM:SS` (e.g., `2023:10:24-15:30:00`)

2. `/home/user/service_b.jsonl`
   Format: `{"ts": "YYYY-MM-DDTHH:MM:SSZ", "key": "...", "src": "..."}`
   The `src` field occasionally contains standard Unicode escape sequences (e.g., `\u00e9`) that must be properly decoded into UTF-8 bytes before any distance calculation. (Assume all escapes are in the Basic Multilingual Plane, i.e., `\uXXXX`).

Your task:
1. Write a C program at `/home/user/merger.c` and compile it to `/home/user/merger`. You may use standard C POSIX libraries. You may use `cJSON` or write your own minimal parser, but you must ensure `\uXXXX` sequences are converted to raw UTF-8 bytes. 
2. Your program must find all pairs of records (one from Service A, one from Service B) that satisfy BOTH of the following conditions:
   - The absolute difference between their timestamps is less than or equal to 5 seconds.
   - The byte-level Levenshtein distance between A's `source_text` and B's decoded `src` text is less than or equal to 3.
3. For each matching pair, output a line to `/home/user/matches.csv` in the exact format:
   `A_loc_key,B_key,time_diff_in_seconds,levenshtein_distance`
   (e.g., `btn_ok,ok_btn,3,2`)
4. Sort the lines in `/home/user/matches.csv` alphabetically by `A_loc_key` before finalizing the file.

Write the code, compile it, and generate the `/home/user/matches.csv` file.