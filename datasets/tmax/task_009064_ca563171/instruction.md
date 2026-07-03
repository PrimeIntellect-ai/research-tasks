You are a Data Engineer debugging a massive ETL (Extract, Transform, Load) pipeline. Recently, the pipeline scheduler has been freezing because several concurrent transactions are entering deadlocks. Upon investigation, you suspect that the workflow metadata has been corrupted, introducing cyclical dependencies into the ETL task graph (which is supposed to be a Directed Acyclic Graph).

Your task is to write a custom query engine in C that parses the dependency graph, matches cyclical patterns (deadlocks), and exports the affected tasks.

1. There is an edge-list CSV file located at `/home/user/etl_dependencies.csv`. Each row contains `source_job,target_job`, meaning `source_job` must complete before `target_job` can start.
2. Write a C program at `/home/user/detect_deadlocks.c` that:
   - Takes exactly two command-line arguments: the input CSV file path and the output CSV file path (parameterized execution).
   - Reads the input graph.
   - Performs graph analytics to find **all** job IDs that are part of *any* directed cycle (representing a deadlock pattern).
   - Exports the results to the output CSV file.
3. The exported output file must:
   - Have a header row: `deadlocked_job_id`
   - List every job ID involved in a cycle exactly once.
   - The job IDs must be sorted in ascending alphabetical order.
4. Compile your program and run it to process `/home/user/etl_dependencies.csv` and output the results to `/home/user/deadlocks_found.csv`.

You may use any standard C libraries (e.g., `stdio.h`, `stdlib.h`, `string.h`). Do not use external non-standard libraries.