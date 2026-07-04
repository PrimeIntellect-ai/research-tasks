I am a log analyst investigating some access patterns, but our custom C log parser is failing. 

We receive daily application logs in JSON-Lines format. I wrote a basic C program, `/home/user/parser.c`, to extract the `"message"` field, convert it to lowercase, and print it. 
However, our logging library recently started escaping non-alphanumeric ASCII characters and some letters as unicode escape sequences (e.g., `\u0021` for `!`, `\u0065` for `e`). My parser doesn't understand these sequences, leaving them raw, which ruins my downstream deduplication scripts!

Your task:
1. Fix `/home/user/parser.c` so that it correctly parses and unescapes `\uXXXX` sequences into their standard ASCII characters (you only need to support the standard ASCII range `\u0020` to `\u007E`). 
2. The program must also lowercase the entire extracted message (including the unescaped characters).
3. The program should output only unique, normalized messages (deduplication). You can handle deduplication within the C program or by wrapping the C program execution in a shell script, but the final output must be deduplicated.
4. Compile your fixed program to `/home/user/bin/log_parser`.
5. Run your solution against `/home/user/logs/raw_logs.jsonl` and save the deduplicated, normalized output to `/home/user/logs/clean_messages.txt`.
6. Schedule a daily cron job to run at exactly 02:00 AM that executes your pipeline (processing `/home/user/logs/raw_logs.jsonl` and saving to `/home/user/logs/clean_messages.txt`).

Please ensure everything is set up correctly. I will verify the contents of `clean_messages.txt` and check your crontab.