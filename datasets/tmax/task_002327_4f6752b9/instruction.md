You are an on-call engineer and have just been paged at 3 AM. The data ingestion pipeline, which processes binary log files uploaded by our clients, has crashed. 

The pipeline consists of a shell script `/home/user/pipeline/process_logs.sh` that feeds files from `/home/user/uploads/` to a C program `/home/user/pipeline/parser`.

Upon inspecting the logs, you notice two issues:
1. The shell script is failing to process certain files because their filenames contain spaces.
2. The `parser` executable is crashing (Segmentation Fault) when it encounters corrupted log files uploaded by clients.

The C source code for the parser is located at `/home/user/pipeline/parser.c`. The binary file format is supposed to have a 4-byte magic string `LOG1`, followed by a 4-byte signed integer `N` representing the number of records, and then `N` records of 16 bytes each. 

Your tasks:
1. Fix `/home/user/pipeline/process_logs.sh` so that it correctly handles filenames with spaces.
2. Debug and fix `/home/user/pipeline/parser.c` so that it handles corrupted input gracefully. Specifically, if the record count `N` is less than 0 or greater than 10000, or if memory allocation fails, the program should print `Corrupted input: <filename>` to standard output and exit with status code 1, instead of crashing.
3. Recompile the C program (`gcc -o parser parser.c`).
4. Clear any existing `/home/user/pipeline/results.txt` and `/home/user/pipeline/error.log`.
5. Run the pipeline script `/home/user/pipeline/process_logs.sh`.
6. Output the successful processing results to a file named `/home/user/final_report.txt` by copying the contents of `/home/user/pipeline/results.txt`.

Ensure your C code fixes handle the corrupted inputs safely without causing any memory leaks or segmentation faults.