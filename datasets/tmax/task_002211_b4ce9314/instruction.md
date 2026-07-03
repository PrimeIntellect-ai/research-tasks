You are helping me organize a massive legacy project. We need to identify the most "structurally complex" files to prioritize refactoring. We have an old, undocumented compiled tool that calculates raw byte entropy, but we need a modern Python service to manage the analysis and ranking.

Your task is to build a Python-based HTTP service that analyzes files, computes a custom metric, and maintains a ranking data structure.

Here are the requirements:

1. **The Legacy Tool (`/app/legacy_scorer`)**:
   - There is a stripped binary located at `/app/legacy_scorer`.
   - It takes a single command-line argument (an absolute file path) and prints a single floating-point number to standard output representing the raw byte entropy of the file.
   - Example: `/app/legacy_scorer /etc/passwd` -> `3.8415`

2. **Numerical Algorithm (Project Complexity Factor - PCF)**:
   - The raw entropy isn't enough. For each file, your Python service must calculate the "Project Complexity Factor" (PCF).
   - Formula: `PCF = raw_entropy * log2( max(file_size_in_bytes, 2) )`
   - Use standard floating-point precision for the calculation.

3. **Custom Data Structure**:
   - To organize the project files efficiently, your service must maintain an in-memory Max-Heap based on the computed PCF score. When ties occur, sort alphabetically by file path.

4. **The Web Service**:
   - Create a Python HTTP service (you may use frameworks like Flask or FastAPI) listening exactly on `127.0.0.1:8080`.
   - **`POST /analyze`**:
     - Accepts a JSON payload: `{"files": ["/absolute/path/1", "/absolute/path/2"]}`
     - For each file, the service should check its size, run `/app/legacy_scorer`, calculate the PCF, and insert it into the Max-Heap.
     - Files that do not exist should be skipped.
     - Returns `{"status": "success", "processed": N}` where N is the number of valid files processed.
   - **`GET /top?n=X`**:
     - Retrieves the top `X` files with the highest PCF from your data structure (without removing them).
     - Returns a JSON list of objects: `[{"path": "/absolute/path/2", "pcf": 45.123}, {"path": "/absolute/path/1", "pcf": 12.5}]` (ordered highest PCF to lowest).

5. **Packaging and Setup**:
   - Write a bash script at `/home/user/setup_and_run.sh` that acts as a deployment script.
   - The script must:
     1. Create a Python virtual environment at `/home/user/venv`.
     2. Activate it and install any required Python dependencies.
     3. Start your web service in the background so that it listens on port 8080.
   - Ensure the script is executable (`chmod +x`).

Implement the service and execute `/home/user/setup_and_run.sh` to leave the service running for verification.