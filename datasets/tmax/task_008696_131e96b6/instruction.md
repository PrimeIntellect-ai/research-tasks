You are a support engineer investigating a severe outage in a distributed system. You have been provided with a diagnostic data processing pipeline located in `/home/user/diagnostics`. The pipeline consists of several scripts written in different languages that process raw logs, compute health metrics, and model system state. However, the pipeline is currently broken and failing at multiple stages.

Your objective is to fix the pipeline so it successfully processes `/home/user/diagnostics/raw_logs.txt` and generates the correct output in `/home/user/diagnostics/final_report.json`.

The pipeline is executed via `/home/user/diagnostics/run_pipeline.sh`, which runs the following phases:

**Phase 1: Dependency Setup (Bash/Python)**
The script attempts to install Python dependencies from `requirements.txt` into a virtual environment at `/home/user/diagnostics/venv`. Currently, it fails due to a dependency conflict.
*Task:* Resolve the conflict in `requirements.txt` so that both `numpy` and `networkx` can be installed successfully without strictly locking versions that are incompatible with each other. You may update the versions to resolve the conflict.

**Phase 2: Log Extraction (Perl)**
The script `extract.pl` reads `raw_logs.txt` and extracts CPU, Memory, and Latency metrics.
*Task:* The script crashes or drops lines when encountering an edge case: sometimes the `latency` field is entirely blank (e.g., `latency=`). 
Fix `extract.pl` so that if the `latency` value is missing, it defaults to `0`. It must output a valid CSV file to `extracted_metrics.csv`.

**Phase 3: Health Score Calculation (Ruby)**
The script `calculate_health.rb` reads `extracted_metrics.csv` and computes a System Health Score for each node.
*Task:* The formula implemented in the script is incorrect due to order-of-operations and missing parentheses. 
The correct mathematical formula for the Health Score is:
`Score = ((100 - CPU) * 0.4) + ((100 - Memory) * 0.4) + ((1000 / (Latency + 1.0)) * 0.2)`
Fix the formula in `calculate_health.rb`.

**Phase 4: State Smoothing (Python)**
The script `topology_smoothing.py` reads the calculated scores and simulates a diffusion process across the network nodes over 50 iterations to find a steady state.
*Task:* The algorithm currently fails to converge (produces `NaN` or `inf` values) because the adjacency matrix `A` is not row-normalized before the iterative updates.
Fix the script by row-normalizing the adjacency matrix `A` (i.e., ensure the sum of each row equals 1) before the main loop begins.

Once you have fixed all the issues, run `/home/user/diagnostics/run_pipeline.sh`.
Your final result will be evaluated based on the exact values in `/home/user/diagnostics/final_report.json`.