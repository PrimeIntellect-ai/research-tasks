You are tasked with building a configuration drift monitoring pipeline. You need to process configuration files originating from different servers in multiple formats, normalize them, compute their drift (similarity) compared to a baseline, and log the results.

All work should be done in `/home/user/workspace/`. 
The configuration files are located in `/home/user/workspace/configs/`:
1. `baseline.txt` - A standard properties file.
2. `server1.json` - A JSON configuration file.
3. `server2.ini` - An INI configuration file.

Here are the exact requirements:

1. **Data Normalization (Shell Scripting):**
   Write a shell script named `/home/user/workspace/pipeline.sh` that extracts the configuration key-value pairs from `server1.json` and `server2.ini`. 
   It must create normalized text files `server1.txt` and `server2.txt` in the `/home/user/workspace/` directory.
   The format of these output files must be exactly:
   `key=value`
   Each file MUST have its keys sorted alphabetically. Ensure there are no spaces around the `=` sign, no quotes around values, and no empty lines. Ensure a trailing newline exists. (e.g., `mode=prod\nport=8080\n`).

2. **Distance Computation (C Programming):**
   Write a C program saved at `/home/user/workspace/calc_drift.c` that reads two text files, treats their entire contents as single strings, and computes the Levenshtein distance between them.
   The program should take three command-line arguments:
   `./calc_drift <baseline_file> <target_file> <target_name>`
   It must append a single line to `/home/user/workspace/drift_report.csv` in the format:
   `<target_name>,<levenshtein_distance>`

3. **Pipeline Logging:**
   Your `pipeline.sh` script must orchestrate the whole process.
   - It should first compile the C program into an executable named `calc_drift`.
   - It should generate the normalized `server1.txt` and `server2.txt`.
   - Before processing a server file with the C program, it must append a log line to `/home/user/workspace/pipeline.log` in the exact format: `[START] Processing <target_name>`
   - It should run the C program for `server1.txt` (with target name `server1`) and `server2.txt` (with target name `server2`) against `baseline.txt` (note: ensure `baseline.txt` is also sorted alphabetically by key before comparison!).
   - After running the C program for a file, it must append to `/home/user/workspace/pipeline.log`: `[END] Processed <target_name>`

Execute your pipeline so the final CSV and log files are generated.