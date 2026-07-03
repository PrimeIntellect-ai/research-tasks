You are tasked with building a configuration change tracking pipeline. A massive stream of configuration changes is continuously dumped into `/home/user/config_stream.csv`. You need to build a data pipeline that processes this file efficiently.

Your objective is to write a C program for validating the data and a Bash script to orchestrate the processing pipeline as a Directed Acyclic Graph (DAG) of tasks.

### 1. Data Validation (C Program)
Create a C program at `/home/user/validate.c` that compiles to `/home/user/validate`. 
It must accept exactly three arguments: `./validate <input_csv> <valid_csv> <invalid_csv>`.
The program should stream the `<input_csv>` line by line (to handle extremely large files without loading everything into memory), check each line against the validation rules (Quality Gates) below, and write the line to `<valid_csv>` if it passes, or `<invalid_csv>` if it fails.

The CSV has no header and contains 6 columns: `timestamp,user,region,config_key,action,value`.
Validation Rules:
1. `timestamp`: Must be a valid integer strictly greater than `1600000000`.
2. `user`: Must not be empty.
3. `region`: Must be exactly 2 characters long.
4. `action`: Must be exactly one of: `ADD`, `MOD`, `DEL`.

Assume no commas exist inside the field values.

### 2. Pipeline Orchestration (Bash Script)
Create a bash script at `/home/user/pipeline.sh` that implements the following DAG:
**Phase 1: Build**
Compile `/home/user/validate.c` to `/home/user/validate` using `gcc -O3`.

**Phase 2: Extract & Split**
Split the main file `/home/user/config_stream.csv` into separate temporary files by the `region` column (e.g., `split_US.csv`, `split_EU.csv`, etc.). 

**Phase 3: Concurrent Transformation**
Run the `./validate` program on each regional split file **concurrently** as background jobs, producing a valid and invalid file for each region (e.g., `valid_US.csv`, `invalid_US.csv`). Use `wait` to ensure all background jobs complete before proceeding.

**Phase 4: Aggregation & Load**
Concatenate all valid outputs into `/home/user/processed_valid.csv`.
Concatenate all invalid outputs into `/home/user/processed_invalid.csv`.
Create a summary file at `/home/user/stats.txt` with exactly the following format:
```
Total Valid: <number>
Total Invalid: <number>
```

Make sure your `pipeline.sh` is executable (`chmod +x`). Once you have written both files, execute `/home/user/pipeline.sh` to produce the final output.