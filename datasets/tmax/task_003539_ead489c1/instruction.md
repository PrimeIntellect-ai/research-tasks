You are an automation specialist tasked with building a multi-stage data processing pipeline to parse, validate, and process messy geospatial coordinate logs. 

System State & Requirements:
1. **Input Data**: You will find log files in `/home/user/incoming_logs/`. (Assume these are created before you start, but you must write your scripts to process whatever `.log` files are present there). 
   Each log file contains text with embedded coordinates in this exact messy format:
   `[TIMESTAMP] Route <route_id>: Departed from (X: <x1>, Y: <y1>) -> Arrived at (X: <x2>, Y: <y2>) | Status: <status>`
   *Note: There might be extra whitespace or text, but the coordinate format `(X: float, Y: float)` is consistent. Some lines are corrupted or lack coordinates.*

2. **Phase 1: Extraction & Validation (Python)**
   Write a Python script `/home/user/extract.py` that reads a given log file and uses regular expressions to extract `route_id`, `x1`, `y1`, `x2`, `y2`, and `status`.
   **Quality Gate**: The script must ONLY output records where `Status: SUCCESS`. Any records with `Status: FAILED` or malformed coordinates must be completely ignored.

3. **Phase 2: Distance Computation (Python)**
   Write a Python script `/home/user/compute.py` that takes the validated records from Phase 1 and computes the Euclidean distance between the start `(x1, y1)` and end `(x2, y2)` points.

4. **Phase 3: Pipeline Orchestration (Bash)**
   Write a bash script `/home/user/pipeline.sh` that ties these together. When executed, it must:
   - Find all `.log` files in `/home/user/incoming_logs/`.
   - Process each file using your Python scripts.
   - Append the successful results to a single CSV file at `/home/user/output_metrics.csv` with the exact header: `route_id,distance` (distance rounded to 2 decimal places).
   - Move the processed `.log` files to `/home/user/archive/`.

5. **Phase 4: Scheduling**
   Create a text file at `/home/user/schedule.cron` containing exactly one line: the valid crontab entry required to run `/home/user/pipeline.sh` every 15 minutes. Use the bash executable explicitly (e.g., `/bin/bash`).

Ensure all scripts are executable. Do not run the pipeline yourself—just leave the scripts and the cron file ready, but to test your solution, you may run `./pipeline.sh` manually. (I will evaluate your final `output_metrics.csv` and scripts).