You are a performance engineer tasked with debugging a batch processing application. 

You have been given a Python script located at `/home/user/process_data.py` that reads a large dataset of measurements from `/home/user/data_inputs.txt`. The script computes the standard deviation of the measurements on each line and writes the results to an output file.

Recently, the script started crashing with a `ValueError: math domain error` before it could finish processing the entire file. The crash is caused by numerical instability and catastrophic precision loss in the custom standard deviation calculation, which occasionally produces negative variances for certain edge-case inputs.

Your task is to debug this issue using delta debugging/test minimization and fix the precision loss problem.

Complete the following steps:
1. **Locate the Failure**: Find the exact line number in `/home/user/data_inputs.txt` that triggers the crash. Write this line number (just the integer digits) to `/home/user/buggy_line_num.txt`.
2. **Minimize the Test Case**: Create a minimal reproducible example script at `/home/user/mre.py`. This script must:
   - Hardcode the exact sequence of numbers from the buggy line as a list of floats named `data`.
   - Contain the buggy standard deviation calculation logic from `process_data.py`.
   - When run, reproduce the exact `ValueError` exception without reading any external files.
3. **Fix the Instability**: Identify the true population standard deviation of the numbers on the buggy line using a numerically stable method. Write this correct value, rounded to 4 decimal places, to `/home/user/stable_result.txt`.

Ensure all requested files are created exactly at the specified paths.