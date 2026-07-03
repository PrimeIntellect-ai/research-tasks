You are a DevOps engineer troubleshooting a crashing internal analytics application. 

You have been given a partial memory snapshot of the crashed process and the application's source code. You need to accomplish two tasks to restore service functionality:

1. **Memory Dump Analysis**: 
   The application crashed before it could log the newly rotated API key. The memory snapshot is located at `/home/user/app/crash_mem.bin`. Analyze this binary file to find the active API key. The key is stored in memory as a string starting with `API_KEY=` followed by a 16-character alphanumeric string. 
   Extract the 16-character key (without the `API_KEY=` prefix) and save it precisely to a new file at `/home/user/solution/api_key.txt`.

2. **Floating-Point Precision Repair**:
   The application crashes in the reporting module due to a strict equality check on floating-point numbers. Examine the file `/home/user/app/report.py`. It currently calculates a sum of fractional transaction values and compares it directly using `==`. 
   Modify `/home/user/app/report.py` so that it uses Python's built-in `math.isclose()` (with default tolerances) to compare the computed sum against the expected total. 
   When fixed, running `python3 /home/user/app/report.py` should output exactly `REPORT_VALID` to standard output.

Ensure the `/home/user/solution` directory is created if it does not exist.