You are a database reliability engineer tasked with analyzing backup job schedules to prevent deadlocks and optimize runtimes.

You have been provided an SQLite database at `/home/user/backups.db` containing two tables:
1. `jobs` (columns: `id` TEXT PRIMARY KEY, `duration` INTEGER) - Contains backup jobs and their baseline durations in minutes.
2. `dependencies` (columns: `job_id` TEXT, `depends_on_id` TEXT) - Contains the dependency edges. A job cannot start until all jobs it depends on have completed.

Write a Python script at `/home/user/analyze_backups.py` that analyzes this database and performs the following:

1. **Deadlock Detection**: Identify any jobs that are part of a circular dependency chain (a deadlock). Write the IDs of all jobs involved in *any* circular dependency to `/home/user/deadlocks.txt`, one per line, sorted alphabetically. 

2. **Total Duration Calculation**: For all jobs that are completely free of deadlocks (meaning the job itself is not in a cycle, and none of its transitive dependencies are in a cycle), calculate the total sequential execution time. The total execution time is the duration of the job itself plus the durations of ALL of its unique transitive dependencies. 
Write these results to `/home/user/durations.txt`, one per line, in the format `[id]: [total_duration]`, sorted alphabetically by job ID.

Ensure your Python script runs successfully and creates the two text files with the correct output.