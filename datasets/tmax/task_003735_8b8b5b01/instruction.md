You are an AI assistant acting as a script developer. We need a utility that merges sensor logs, decodes them, calculates an anomaly score using a fast C backend, sorts the results, and writes them out. We also require a suite of unit tests.

Please complete the following tasks:

1. **C Backend Implementation (FFI & Numerical Algorithm):**
   Create a C file at `/home/user/anomaly.c`. It must contain a single exposed function:
   `double compute_anomaly_score(double* values, int length);`
   This function must compute the Root Mean Square (RMS) of the provided array.
   Formula: `RMS = sqrt( (v_1^2 + v_2^2 + ... + v_n^2) / n )`.
   Compile this C code into a shared library located at `/home/user/libanomaly.so`. 

2. **Python Utility script (Encoding, Merging, Sorting, FFI):**
   Write a Python script at `/home/user/process_logs.py` that performs the following steps:
   - Reads two input files: `/home/user/data1.txt` and `/home/user/data2.txt`. Both files are encoded in **UTF-16**.
   - Each line in these files is formatted as `SensorID,val1,val2,val3...` where values are floats.
   - Merges the records from both files into a single collection.
   - Loads `/home/user/libanomaly.so` using Python's `ctypes` module.
   - For each sensor, passes the array of float values to `compute_anomaly_score` via `ctypes` to get the RMS anomaly score.
   - Sorts the sensors based on their anomaly score in **descending** order. If two sensors have the exact same score, sort them alphabetically by SensorID in ascending order.
   - Writes the sorted results to `/home/user/merged_anomalies.txt` using **UTF-8** encoding. 
   - The output file must contain exactly one line per sensor in the format: `SensorID: <score>` where the score is formatted to exactly 4 decimal places (e.g., `SENS_X: 3.5355`).

3. **Unit Testing:**
   Write a Python unit test script at `/home/user/test_process.py` using the built-in `unittest` framework.
   - It must include at least one test class extending `unittest.TestCase`.
   - It must load `libanomaly.so` and test `compute_anomaly_score` directly.
   - It should test that an input array of `[3.0, 4.0]` returns an RMS score of approximately `3.5355339`.
   
4. **Execution:**
   - Run your Python utility script to generate `/home/user/merged_anomalies.txt`.
   - Run your unit tests and redirect both stdout and stderr to `/home/user/test_results.log` (e.g., `python3 test_process.py > /home/user/test_results.log 2>&1`).

Ensure all files are created in the `/home/user` directory. You have all necessary tools (gcc, python3) available.