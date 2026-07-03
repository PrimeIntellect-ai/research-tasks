You have inherited an unfamiliar, legacy data processing pipeline written in Bash. The pipeline consists of two services that process data sequentially, but the pipeline is currently failing due to corrupted inputs. The previous developer left behind some logs from the last failed run, but no documentation.

Your objectives are to reconstruct the event timeline, identify the corrupted inputs causing the crashes, fix the data validation logic, and successfully run the pipeline.

Here is the setup:
- `/home/user/app/raw_data.csv`: The input data file.
- `/home/user/app/service_a.sh`: Reads the CSV, validates it, and writes to a named pipe.
- `/home/user/app/service_b.sh`: Reads from the named pipe and aggregates the results.
- `/home/user/app/run_pipeline.sh`: Starts both services.
- `/home/user/logs/service_a.log` and `/home/user/logs/service_b.log`: Logs from the last crashed run.

Task Requirements:
1. **Log Timeline Reconstruction**: The two log files use slightly different timestamp formats. `service_a.log` uses `YYYY-MM-DD HH:MM:SS` while `service_b.log` uses Epoch timestamps (seconds since 1970). 
   Write a script to merge these two log files, convert all timestamps to Epoch format, sort them chronologically, and output the result to `/home/user/merged_timeline.log`. Each line should be formatted as: `<epoch_timestamp> [<SERVICE_NAME>] <original_log_message_without_timestamp>`. (Service names should be `SERVICE_A` and `SERVICE_B`).

2. **Error Diagnosis**: By inspecting the merged timeline, identify the `id`s of the records that caused `service_b.sh` to crash. Write these `id`s, one per line, sorted numerically, into `/home/user/corrupted_ids.txt`.

3. **Fix the Code**: The crashes are caused by a flawed validation logic in `/home/user/app/service_a.sh`. Currently, it attempts to filter out records where the `value` column is not a strictly positive integer, but the Bash regex/logic used is incorrect and lets some corrupted values through. 
   Modify `/home/user/app/service_a.sh` so that it correctly identifies and skips any record where the `value` is not a strictly positive integer (e.g., it must reject floats, negative numbers, empty strings, and strings with special characters).

4. **Run the Pipeline**: Once fixed, execute `/home/user/app/run_pipeline.sh`. It will process `/home/user/app/raw_data.csv` and generate `/home/user/app/final_output.txt`.

Ensure all requested files (`merged_timeline.log`, `corrupted_ids.txt`, `final_output.txt`) are present in their exact specified locations.