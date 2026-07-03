You are an operations engineer triaging an incident with a critical data processing daemon. The C program `/home/user/telemetry_app/telemetry_processor.c` is responsible for parsing text-based telemetry logs from the `/home/user/telemetry_app/data/` directory.

However, the pipeline has been failing recently, and your monitoring system shows three distinct issues with this binary:
1. **Inconsistent Results:** When run multiple times over the same data, the final `global_records_processed` count varies, indicating a concurrency issue.
2. **Hangs:** The program sometimes consumes 100% CPU and hangs indefinitely on specific log files.
3. **Crashes:** The program occasionally aborts with a segmentation fault due to a buffer overflow when processing abnormally long telemetry tokens.

Your task is to:
1. Debug and fix the source code in `/home/user/telemetry_app/telemetry_processor.c` so that it safely and accurately processes all files in the `data` directory without hanging, crashing, or dropping counts.
2. Recompile the program using `gcc -pthread telemetry_processor.c -o telemetry_processor`.
3. Run the compiled program against the `/home/user/telemetry_app/data/` directory.
4. The program will print out the final processed record count. Save this output directly to `/home/user/telemetry_app/final_count.txt`.

The automated test will verify the contents of `/home/user/telemetry_app/final_count.txt` to ensure the final record count is exactly correct. The file must contain only the output produced by the fixed program (e.g., `Total records: <number>`).