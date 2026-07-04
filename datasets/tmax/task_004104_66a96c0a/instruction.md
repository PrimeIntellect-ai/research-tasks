You are a Data Engineer tasked with analyzing an ETL pipeline's metadata. Our pipeline execution engine uses a local SQLite database to track job definitions, their dependencies (forming a Directed Acyclic Graph, ideally), and historical execution logs. Recently, the pipeline scheduler has been freezing, and we suspect some developers accidentally introduced cyclic dependencies (deadlocks) into the job configurations.

The database is located at `/home/user/etl_metadata.db` and has the following schema:
- `jobs` (`job_id` INTEGER PRIMARY KEY, `job_name` TEXT)
- `dependencies` (`job_id` INTEGER, `depends_on_job_id` INTEGER) - Represents that `job_id` must run *after* `depends_on_job_id`.
- `executions` (`execution_id` INTEGER PRIMARY KEY, `job_id` INTEGER, `start_time` DATETIME, `end_time` DATETIME, `status` TEXT)

Your task is to write the necessary SQL queries (which you can execute via the `sqlite3` CLI) to analyze this data and produce two output files:

**1. Identify Cyclic Dependencies (Deadlocks)**
Find all jobs that are part of a dependency cycle.
Create a file at `/home/user/cyclic_jobs.txt` containing the `job_name` of every job involved in *any* cycle. Output one job name per line, sorted alphabetically.

**2. Calculate Job Execution Statistics**
For all jobs that are **NOT** part of any cycle, we need to analyze their execution history to optimize scheduling.
Create a CSV file at `/home/user/job_stats.csv` with the following columns (include the header):
`job_name,avg_duration_seconds,hierarchy_level`

Where:
- `job_name`: The name of the job.
- `avg_duration_seconds`: The average execution duration (in seconds) of the **last 3 successful** executions for this job. Use the `start_time` and `end_time` to calculate duration. (If a job has fewer than 3 successful executions, average the ones available. If it has 0, output 0). *Hint: You will need a window function to isolate the last 3 runs ordered by `start_time` descending.*
- `hierarchy_level`: The maximum depth of the job in the dependency graph. A root job (depends on nothing) is at level 0. A job that depends directly on a root job is at level 1, and so on.

Order the resulting CSV by `hierarchy_level` ascending, then `job_name` ascending. Round the `avg_duration_seconds` to the nearest whole integer.