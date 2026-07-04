You are a data engineer debugging a deadlocked ETL pipeline scheduler. The pipeline tasks and their execution dependencies are defined in a text file, but a cyclical dependency has been accidentally introduced, causing a deadlock where tasks wait on each other indefinitely.

You have been provided with two files in your home directory:
1. `/home/user/etl_graph.txt`: A space-separated file representing the directed edges of the ETL dependency graph. Each line contains `TaskA TaskB`, meaning `TaskA` must complete before `TaskB` can start.
2. `/home/user/etl_metadata.csv`: A comma-separated values file containing metadata for each task in the format `TaskID,TaskType,Description`.

Your objective is to use standard Linux command-line tools to analyze the graph, find the deadlock, and extract information about the affected tasks:

1. Identify the tasks involved in the dependency cycle (the deadlock) within `/home/user/etl_graph.txt`.
2. Extract the unique IDs of the tasks involved in this cycle, sort them alphabetically, and save them (one per line) to `/home/user/cycle_tasks.txt`.
3. For the tasks identified in the cycle, look up their metadata in `/home/user/etl_metadata.csv`. Filter out only the tasks that have a `TaskType` of exactly `Transformation`.
4. Extract the `Description` field of these Transformation tasks, sort the descriptions alphabetically, and save them (one per line) to `/home/user/deadlocked_descriptions.txt`.

Ensure your final output files exactly match the requested formats and are placed in the correct paths.