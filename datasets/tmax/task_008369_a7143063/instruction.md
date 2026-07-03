You are a DevOps engineer debugging a log processing pipeline. 

There is a shell script at `/home/user/process_logs.sh` that iterates over log files in the `/home/user/logs/` directory and calls a Python script `/home/user/process.py` to count the occurrences of the word "ERROR" in each file. 

However, the pipeline is currently broken:
1. The shell script breaks when encountering filenames with spaces.
2. The Python script crashes with a `UnicodeDecodeError` when reading logs that contain corrupted or non-UTF-8 bytes.

Your tasks:
1. Fix `/home/user/process_logs.sh` so that it correctly passes filenames with spaces to the Python script.
2. Fix `/home/user/process.py` to handle corrupted files gracefully. It must read the files, ignore any invalid Unicode characters, and successfully count the occurrences of "ERROR".
3. Run the fixed `/home/user/process_logs.sh`. The final total count of errors will be stored in `/home/user/total_errors.txt`.
4. Create a Minimal Reproducible Example (MRE) at `/home/user/mre.py`. This script should:
   - Create a dummy file named `/home/user/mre_test.log` containing a non-UTF-8 byte (e.g., `\xff`).
   - Attempt to open and read the file in default text mode.
   - Catch the resulting `UnicodeDecodeError`.
   - Print exactly the string `"Traceback interpreted correctly"` when the exception is caught.

Ensure that after your fixes, running `/home/user/process_logs.sh` processes all files in the directory and produces the correct aggregated total in `/home/user/total_errors.txt`.