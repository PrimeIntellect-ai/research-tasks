You are a data analyst tasked with processing a dataset of 3D coordinates, performing mathematical grouping, and orchestrating a simple data pipeline.

We have a CSV file located at `/home/user/data/points.csv` containing 3D points. The file has the header `id,x,y,z`.

Your task involves writing code, orchestrating it, and preparing it for scheduling:

1. **Mathematical Processing Script**: Write a Python script at `/home/user/process_math.py` that reads the CSV file. 
   - For each point, calculate the Euclidean distance from the origin (0,0,0).
   - Compute the floor of this distance (round down to the nearest integer). Let's call this integer `D`.
   - Group the point `id`s by their `D` value.
   - For each group `D`, sort the list of `id`s in ascending numerical order.
   - Write the resulting groups to a JSON file at `/home/user/output/grouped.json`. The JSON should be a dictionary where the keys are the integer `D` values (as strings, per JSON standard) and the values are the sorted lists of integer `id`s.

2. **Pipeline Orchestration & Data Transfer**: We need to treat the computation and a subsequent backup as a Directed Acyclic Graph (DAG). Write a bash script at `/home/user/run_pipeline.sh` that:
   - Executes your Python script.
   - After successful execution, transfers (copies) the resulting `/home/user/output/grouped.json` to a simulated remote backup location: `/archive/remote_backup/grouped.json`. 
   - Make sure the bash script is executable.

3. **Pipeline Scheduling**: The pipeline needs to run automatically. Create a file `/home/user/cron_schedule.txt` that contains exactly one line representing the crontab entry (cron expression and command) required to run `/home/user/run_pipeline.sh` at exactly 2:30 AM every day. Run it as the `user` user. 

Make sure you create any necessary output directories in your bash script if they don't already exist.