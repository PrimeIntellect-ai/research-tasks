You are a capacity planner analyzing filesystem resource usage for a custom container runtime. Your task is to write a C++ program to analyze the filesystem usage of various mock containers, automate the execution with a robust bash script, and successfully push the metrics to a local reporting service. 

Currently, attempts to push metrics to the reporting service silently fail or are rejected, similar to an SSH configuration that silently rejects key-based logins. You must diagnose and fix this connectivity/authentication issue.

Here are the specific requirements:

1. **C++ Analyzer (`/home/user/analyzer.cpp`)**:
   - Write a C++ program that uses standard library features (like `<filesystem>`) to scan the directory `/home/user/mock_containers/`.
   - The `mock_containers` directory contains subdirectories representing container IDs (e.g., `alpha`, `beta`, `gamma`).
   - For each container, calculate the total size (in bytes) of all files recursively located *only* inside its `data/` subdirectory. Ignore files outside the `data/` folder.
   - The program must write the results to `/home/user/capacity_report.csv`.
   - The CSV format must have exactly two columns: `container_id,size_bytes`, sorted alphabetically by `container_id`.

2. **Diagnose and Fix Reporting Connectivity**:
   - A local reporting service is running on `http://127.0.0.1:9090`.
   - The service accepts POST requests to `/upload` containing the CSV file.
   - However, your client configuration at `/home/user/.config/reporter/auth.conf` is currently misconfigured, causing the server to silently drop or reject the payload.
   - Inspect the server's requirements (the server code is available at `/home/user/reporting_service.py` if you need to debug) and fix your local `auth.conf` so requests are accepted. 

3. **Automation Script (`/home/user/submit_metrics.sh`)**:
   - Write a bash script that handles the end-to-end process.
   - It should compile the C++ code to `/home/user/analyzer` using `g++` (ensure standard C++17 or C++20 is used).
   - It should execute the compiled analyzer and verify that the CSV file was created successfully.
   - It should parse the corrected token from `/home/user/.config/reporter/auth.conf` and use `curl` to POST the CSV file to `http://127.0.0.1:9090/upload` with the header `X-Auth-Token: <token>`. Include the CSV content as the raw POST body.
   - The script must exit with code 0 on success and non-zero if any step fails.

Ensure all file paths match exactly. Once you have written the code, run your `/home/user/submit_metrics.sh` script to complete the task.