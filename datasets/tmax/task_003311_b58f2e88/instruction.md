You are a Database Reliability Engineer managing a complex, distributed database backup system. The backup scheduler relies on a metadata store that records execution dependencies between various backup jobs (e.g., table A must be backed up before table B). 

Recently, the backup system completely halted. You suspect that recent automated schema migrations introduced a "deadlock"—a circular dependency where two or more backup jobs are waiting on each other indefinitely.

The backup job metadata has been exported for you into a JSONL (JSON Lines) file located at `/home/user/backup_jobs.jsonl`. Each line is a NoSQL-style JSON document representing a backup job and an array of `job_id`s it directly depends on.

Your task is to write a Python script (e.g., `/home/user/resolve_backups.py`) that performs graph analytics on this dataset to achieve two goals:

1. **Deadlock Detection**: Identify all cyclic dependencies in the backup graph. 
   - Output the cycles to `/home/user/deadlocks.json`.
   - The format must be a list of lists of strings. Each inner list represents a cycle.
   - To ensure a deterministic output, sort the `job_id`s within each cycle alphabetically, and then sort the list of cycles by their first elements.

2. **Hierarchical Scheduling**: For all jobs that are *not* part of a deadlock and are *not* dependent (directly or indirectly) on a deadlocked job, compute their backup tiers.
   - Tier 0 consists of jobs with NO dependencies.
   - Tier 1 consists of jobs that depend ONLY on Tier 0 jobs, and so forth.
   - Output this schedule to `/home/user/valid_schedule.json`.
   - The format must be a JSON object mapping the tier number (as a string, e.g., `"0"`, `"1"`) to an alphabetically sorted list of `job_id`s belonging to that tier.

You may use any standard Python libraries or install third-party graph analytics libraries (like `networkx`) using `pip` to solve this. Make sure your Python script produces exactly the two JSON files requested.