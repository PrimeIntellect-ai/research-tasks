You are a performance engineer tasked with optimizing and debugging a buggy data processing pipeline. 

There is a Python script located at `/home/user/process_sensors.py`. It is designed to read a batch of sensor data files from `/home/user/sensor_data/`, extract an array of integers under the `"values"` key from each file, and calculate the total sum across all files.

However, the pipeline is currently failing for two reasons:
1. **Deadlock / Starvation:** The script uses a `ThreadPoolExecutor`, but it hangs indefinitely. This is due to a classic concurrency bug related to how tasks and sub-tasks are submitted to the same executor.
2. **Corrupted Input Handling:** Some files in the dataset are corrupted (invalid JSON). The script currently gets stuck in an infinite retry loop (livelock) when it encounters them.

Your task is to debug and fix the script. Follow these requirements:
1. Create a fixed version of the script and save it to `/home/user/process_sensors_fixed.py`.
2. Fix the concurrency bug so that the script successfully processes all files without hanging. You may restructure how sub-tasks are executed, but you must still use `concurrent.futures` to parallelize the file processing.
3. Fix the corrupted input handling. When a corrupted file (e.g., `json.JSONDecodeError`) is encountered, the script should catch the error, append the base filename (e.g., `sensor_14.json`) to a log file at `/home/user/bad_files.txt` (one filename per line), and continue processing other files without hanging.
4. The fixed script must output the final sum of all valid files to `/home/user/final_aggregate.json` in the format: `{"total": <sum_of_all_values>}`.

Execute your fixed script to ensure it generates `/home/user/bad_files.txt` and `/home/user/final_aggregate.json` correctly.