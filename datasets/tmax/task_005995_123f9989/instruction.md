You are a log analyst investigating anomalous server behaviors. You have been given a large, raw text log file and need to extract a stratified sample for bulk database import, while maintaining a strict pipeline log of the processing steps. 

Because performance is important for our future data pipelines, you must write the log parsing and sampling utility in C.

**Input:**
A raw log file is located at `/home/user/raw_logs.txt`. 
Each line follows this exact format:
`[YYYY-MM-DD HH:MM:SS] [IP_ADDRESS] [STATUS_CODE] [MESSAGE]`
Example: `[2023-10-24 15:32:01] [192.168.1.55] [404] [Not Found]`

**Requirements:**
1. Write a C program at `/home/user/process_logs.c` and compile it to `/home/user/process_logs`.
2. The program must read `/home/user/raw_logs.txt`.
3. **Stratified Sampling:** Extract exactly the *first* 5 log entries with a 2xx status code, the *first* 5 with a 4xx status code, and the *first* 5 with a 5xx status code (15 lines total).
4. **Database Bulk Export Format:** The extracted logs must be written to a CSV file at `/home/user/import_ready.csv`. 
   - The CSV must have this exact header line: `timestamp,ip_address,status_code,message`
   - The timestamp should combine the date and time (e.g., `2023-10-24 15:32:01`).
   - The CSV rows should not contain the enclosing brackets `[` and `]`.
   - The rows should be written in the exact order they were extracted (i.e., as they appeared in the raw log file).
5. **Pipeline Logging:** As your C program runs, it must append a summary to `/home/user/pipeline.log` exactly matching this format:
   `[PROCESS_LOG] Stratification complete: 5 2xx, 5 4xx, 5 5xx extracted.`
   (If the file had fewer than 5 of any category, the actual counts should be printed, but the test file will have enough).

Write the C code, compile it, and run the pipeline to generate `/home/user/import_ready.csv` and update `/home/user/pipeline.log`. Do not use external C libraries outside of the standard library (e.g., `stdio.h`, `stdlib.h`, `string.h`).