You are an operations data analyst managing a fleet of servers. Due to strict security constraints on your current jumpbox, you do not have access to Python, R, or any external data science libraries. You must perform data transformation, model reconstruction, and inference using ONLY standard Linux command-line tools (Bash, awk, sed, coreutils, etc.).

You have been provided with two files in your home directory (`/home/user/`):
1. `servers.csv`: A raw dataset of server metrics.
2. `model_spec.txt`: A text file containing the configuration and weights for a linear risk assessment model.

Your task is to write a shell script or a pipeline of shell commands to process the data, apply the model, and generate a final report.

### Data Details
`servers.csv` has the following columns:
`ServerID,OS,CPU_Load,Mem_Used_MB,Disk_IOPS`

Some rows contain missing values (represented by consecutive commas, e.g., `srv_002,Linux,,8192,100`). 

### Task Requirements
1. **Data Cleaning (Tabular transformation):** 
   - Parse `servers.csv` (skipping the header).
   - If any numeric field (`CPU_Load`, `Mem_Used_MB`, `Disk_IOPS`) is missing/empty, replace it with `0`.
2. **Model Reconstruction:**
   - Dynamically parse `model_spec.txt` to extract the bias, the categorical weights for the `OS` column, and the continuous weights for `CPU_Load`, `Mem_Used_MB`, and `Disk_IOPS`. 
   - Extract the `ALERT_THRESHOLD`.
3. **Inference (Regression and Classification):**
   - For each server, calculate the `RiskScore` using the formula:
     `RiskScore = (OS_Weight) + (CPU_Load * CPU_Weight) + (Mem_Used_MB * Mem_Weight) + (Disk_IOPS * Disk_Weight) + BIAS`
   - Determine the `Alert` status (Classification): If `RiskScore >= ALERT_THRESHOLD`, then `Alert=1`, else `Alert=0`.
4. **Aggregation and Output:**
   - Format the `RiskScore` to exactly 2 decimal places.
   - Sort the resulting data by `RiskScore` in **descending** numerical order.
   - Save the final output to `/home/user/predictions.csv`.
   - The output file must include a header: `ServerID,RiskScore,Alert`.

Ensure your solution works programmatically (i.e., do not hardcode the model weights into your awk/bash script; your script should read them from `model_spec.txt`).