You are tasked with restoring a backend service and optimizing a critical log analysis task.

Currently, a frontend HTTP proxy is running but returning 502 Bad Gateway errors because the backend service is down. 

1. **Fix the Vendored Backend:**
The backend application source code is pre-vendored at `/app/api-server/`. It uses `gunicorn` to run a Python WSGI app. However, it crashes on startup due to a configuration error in `/app/api-server/gunicorn.conf.py`. The daemon attempts to bind to a root-owned directory. 
Identify the perturbation, patch the configuration to bind to `/home/user/run/backend.sock`, and start the gunicorn daemon in the background from the `/app/api-server/` directory.

2. **Optimize Log Analysis:**
An unoptimized bash script located at `/app/slow_analyzer.sh` processes a massive log file (`/home/user/data/large_access.log`) to calculate the average latency of all requests that resulted in a 502 status code. 
Because it relies on bash `while read` loops and subshells, it is incredibly slow.

Write a highly optimized bash script (using efficient text-processing tools like `awk`, `sed`, or `grep`) and save it to `/home/user/fast_analyzer.sh`.
- It must take no arguments.
- It must read `/home/user/data/large_access.log`.
- It must output *exactly* the same single floating-point number (formatted to 2 decimal places, e.g., `45.23`) as `/app/slow_analyzer.sh`.
- Make sure your script is executable.

An automated verifier will measure the execution time of your script against the baseline. Your script must achieve a **speedup >= 10.0x**.