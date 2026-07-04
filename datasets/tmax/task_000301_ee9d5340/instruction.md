You are an engineer tasked with porting a legacy system telemetry tool to work in a minimal Linux container environment. The original tool relied on heavy bash scripting and a standalone compiled C executable. To minimize dependencies and improve maintainability, you need to port this to a single Python script that interfaces directly with the C logic via a shared library.

You have been provided with the following legacy files in `/home/user/legacy/`:
1. `math_ops.c`: Contains the core calculation logic in a function with the following signature:
   `double calculate_score(double load1, double load5, double load15, long mem_total, long mem_free);`
2. `telemetry.sh`: The old bash script that parsed system files and passed them to the C executable.

Since you are running in a constrained environment, we cannot parse the real `/proc` filesystem. Instead, you must parse mock telemetry files located in `/home/user/mock_proc/`:
- `/home/user/mock_proc/loadavg`: Contains standard load average metrics (e.g., `1.20 1.05 0.90 1/150 1234`).
- `/home/user/mock_proc/meminfo`: Contains memory statistics in the standard Linux format (e.g., `MemTotal:        8192000 kB`).

Your tasks are as follows:
1. Compile `/home/user/legacy/math_ops.c` into a shared library named `libmathops.so` located in `/home/user/py_telemetry/`.
2. Write a Python script `/home/user/py_telemetry/telemetry.py` that:
   - Reads the mock `loadavg` to extract the 1-minute, 5-minute, and 15-minute load averages (first three float values).
   - Reads the mock `meminfo` to extract `MemTotal` and `MemFree` (in kB, parsed as longs).
   - Loads `libmathops.so` using the `ctypes` library and calls `calculate_score` with the extracted values.
   - Evaluates the returned score. If the score is less than 50.0, the status is `"CRITICAL"`, otherwise it is `"OK"`.
3. The script must output a strictly formatted JSON file to `/home/user/telemetry_out.json` containing the exact following structure:
   ```json
   {
       "metrics": {
           "load1": <float>,
           "load5": <float>,
           "load15": <float>,
           "mem_total_kb": <long>,
           "mem_free_kb": <long>
       },
       "score": <float, rounded to 2 decimal places>,
       "status": "<CRITICAL or OK>"
   }
   ```

Constraints:
- You must use the `ctypes` library in Python to link and execute the C function. Make sure to define `argtypes` and `restype` properly for `calculate_score`.
- You cannot use any third-party Python packages (e.g., no `pandas` or `numpy`). Only use the Python standard library.
- When compiled, the shared library must be dynamically linked and loadable by your Python script.
- Execute your script so that `/home/user/telemetry_out.json` is generated successfully.