You are an automation specialist building a streamlined data ingestion pipeline. You have raw sensor logs in `/home/user/data/` that contain duplicate readings across different streams, and the timestamps are not aligned. 

Your objective is to build a hybrid C and Bash pipeline that aligns timestamps, hashes payloads for privacy/deduplication, and produces a clean, deduplicated dataset.

Step 1: Write a C program at `/home/user/align_hash.c` that acts as a standard Unix filter (reads from `stdin`, writes to `stdout`).
- The input will be CSV lines in the format: `timestamp,sensor_id,payload` (e.g., `2023-10-25T14:32:45Z,S1,battery_low`).
- **Timestamp Alignment:** The program must parse the timestamp and align it *down* to the nearest minute by replacing the seconds with `00` (e.g., `2023-10-25T14:32:45Z` becomes `2023-10-25T14:32:00Z`).
- **Hashing:** The program must compute the standard DJB2 hash of the `payload` string. Use this exact algorithm (starting with 5381, multiplying by 33, using `unsigned long`).
- **Output:** For each input line, print a CSV line to `stdout` in the format: `aligned_timestamp,sensor_id,payload_hash` (printing the hash as an unsigned long using `%lu`).

Step 2: Compile the C program to `/home/user/align_hash`.

Step 3: Write a Bash script at `/home/user/run_pipeline.sh` that orchestrates the data flow.
- The script should read all `.csv` files in `/home/user/data/`.
- Pipe the combined data through your `/home/user/align_hash` executable.
- Perform hash-based deduplication to remove duplicate output lines using standard Unix utilities.
- Sort the final deduplicated lines alphabetically.
- Write the final output to `/home/user/final_output.csv`.

Ensure your C program cleanly handles lines up to 256 characters long.