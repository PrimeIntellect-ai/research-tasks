You are a data engineer troubleshooting an ETL pipeline that keeps freezing due to deadlocks. The ETL pipeline's execution history is logged in a SQLite database at `/home/user/etl.db`.

Your task is to identify the tasks causing the deadlock by finding dependency cycles in the *latest* configuration of the pipeline.

The database contains a single table:
`task_runs (run_id INTEGER, task_id INTEGER, depends_on INTEGER, execution_time DATETIME)`

Some tasks are run multiple times and their dependencies (`depends_on`) may change between runs. You must:
1. Write a shell script at `/home/user/run_analysis.sh` that extracts the *latest* run for each `task_id` (based on `execution_time`) using a SQL Window Function (`ROW_NUMBER()`). 
2. The script should export this filtered graph (just `task_id` and `depends_on` where `depends_on` is not NULL) to `/home/user/latest_deps.csv` in CSV format (no headers).
3. Write a C++ program at `/home/user/find_cycle.cpp` that reads `/home/user/latest_deps.csv`, builds a directed dependency graph, and detects the cycle (the deadlock).
4. The C++ program should output the IDs of the tasks involved in the cycle as a comma-separated list, sorted in ascending numerical order, to `/home/user/deadlock.txt`. 
5. The shell script `/home/user/run_analysis.sh` should compile the C++ program (using `g++ -std=c++17`) and execute it.

Ensure your shell script automates the entire process (SQL export -> C++ compilation -> execution).

Example of `/home/user/deadlock.txt` if the cycle involves tasks 7, 5, and 9:
`5,7,9`