You are a data engineer building and debugging an ETL pipeline. Recently, the pipeline scheduler has been hanging due to cyclical dependencies (which cause execution deadlocks).

You have been given an export of the current job dependencies in a CSV file located at `/home/user/etl_dependencies.csv`. The CSV has two columns: `dependent_job` and `upstream_job`. Data flows from the `upstream_job` to the `dependent_job` (i.e., the directed edge should be `upstream_job` -> `dependent_job`).

Your task is to identify the most critical bottleneck job that is part of a deadlock (cycle). Write a Python script to do the following:
1. Load the CSV into a directed graph using the `networkx` library.
2. Identify all jobs (nodes) that are part of at least one directed cycle.
3. Calculate the Betweenness Centrality for *all* nodes in the entire graph. (Use the default parameters for `networkx.betweenness_centrality`, which normalizes the values).
4. Among the jobs that are part of a cycle, find the one with the highest Betweenness Centrality score. If there is a tie, pick the one that comes first alphabetically.
5. Output your finding to a text file at `/home/user/bottleneck.txt`. The file should contain exactly one line with the job name and its centrality score rounded to 4 decimal places, separated by a comma (e.g., `JobName,0.1234`).

Ensure your final answer is written exactly to `/home/user/bottleneck.txt`. You can use the terminal to install any necessary Python packages and run your code.