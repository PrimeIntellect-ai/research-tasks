You are a data engineer working on an ETL pipeline. We receive thousands of noisy log files daily. Your task is to extract, normalize, and deduplicate specific product codes from a batch of raw text logs.

Because performance is critical, you must write a small, efficient C program to handle the string extraction and normalization, and then use shell tools to parallelize the processing of the files.

Step 1: Write a C program at `/home/user/extractor.c` and compile it to `/home/user/extractor`. 
The program must:
- Read text from standard input (stdin) line by line.
- Find all whitespace-separated "words" that match the exact product code format: exactly three uppercase letters, followed by a dash, followed by exactly four digits (e.g., `XYZ-1234`, `ABC-9876`). Do not extract substrings of larger words (e.g., ignore `AXYZ-1234` or `XYZ-12345`). You may use `<regex.h>` or manual string parsing.
- Convert the extracted product codes to fully lowercase (e.g., `xyz-1234`).
- Print each normalized code to standard output (stdout), one per line.

Step 2: Apply your program to the raw data.
- The raw log files are located in the directory `/home/user/raw_logs/`.
- Use a bash pipeline to pass the contents of all `.log` files in this directory to your C program.
- You MUST process the files in parallel using at least 4 concurrent jobs (e.g., using `xargs -P` or `xargs --max-procs`).
- Deduplicate the final normalized codes.
- Sort them alphabetically and save the final output to `/home/user/unique_product_codes.csv`.