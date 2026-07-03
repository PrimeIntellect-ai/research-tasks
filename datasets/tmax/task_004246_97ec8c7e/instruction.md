You are tasked with building a configuration audit pipeline for our infrastructure. Over time, server configurations drift, and we need to track these changes, detect anomalous modifications, and generate an audit report.

The system state and your tasks are as follows:

1. **Input Data**: 
   There is a directory `/home/user/config_data` containing subdirectories for three servers: `server_alpha`, `server_beta`, and `server_gamma`. Inside each, there are daily configuration snapshots in JSON format named `config_YYYY-MM-DD.json`.

2. **Drift Score Calculation**:
   You must write a Python script `/home/user/audit_configs.py` that reads these configurations in chronological order for each server and calculates a "Drift Score" between consecutive days (e.g., Day 1 to Day 2, Day 2 to Day 3).
   
   To calculate the Drift Score between Config A (previous day) and Config B (current day):
   - First, flatten both JSON objects so that nested keys become a single dot-separated key (e.g., `{"network": {"port": 80}}` becomes `{"network.port": 80}`).
   - For every unique key present in either flattened Config A or flattened Config B:
     - If the key is missing in either A or B: add **10** to the score.
     - If the key is in both, but the values are of different types (e.g., int vs string): add **20** to the score.
     - If the key is in both and values are the same type:
       - If they are numeric (int/float): add the absolute difference between the values (e.g., `abs(vA - vB)`) to the score.
       - If they are strings or booleans and are NOT equal: add **5** to the score.
       - If they are equal, add **0**.

3. **Anomaly Detection & Aggregation**:
   - Any day-to-day transition with a Drift Score **strictly greater than 50** is flagged as an "Anomaly".
   - For each server, calculate:
     - `total_anomalies`: The count of anomalous transitions.
     - `average_drift`: The mean Drift Score across all day-to-day transitions for that server. (If there are 3 days, there are 2 transitions. Average drift = sum of those 2 drift scores / 2). Round this to 1 decimal place.

4. **Report Generation**:
   Generate an HTML report using Jinja2. A template is provided at `/home/user/report_template.html`.
   Your script must render this template with the aggregated data and save the output to `/home/user/audit_report.html`.

   The template expects a variable named `servers` which is a dictionary mapping the server name to a dictionary of its stats: `{"server_alpha": {"total_anomalies": X, "average_drift": Y}, ...}`.

Write and execute `/home/user/audit_configs.py` to produce the final `/home/user/audit_report.html`. Install any necessary Python packages (like `jinja2`) yourself.