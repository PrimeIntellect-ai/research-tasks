You are acting as a Database Reliability Engineer. We have a legacy system backup process that frequently deadlocks or takes too long when dumping our database due to concurrent table extraction. 

We have a stripped binary at `/app/backup_scheduler` which simulates our custom backup engine. It accepts a JSON file containing a list of parameterized table extraction jobs and their concurrency groupings. 
If the groupings violate foreign-key constraints (which causes deadlocks in our system) or are inefficient, the binary will output a high total execution latency or report deadlocks.

Your task:
1. Reverse-engineer the data model from the SQLite database located at `/home/user/production.db`.
2. Project this relational schema into a dependency graph (tables as nodes, foreign keys as directed edges).
3. Write a Python script `/home/user/generate_plan.py` that maps the schema graph into an optimized execution plan (a JSON file). 
4. The JSON file must be saved as `/home/user/backup_plan.json`. Its format must be a list of lists, where each inner list contains table names that can be backed up concurrently in that phase.
   Example format: `[["users", "roles"], ["user_roles"], ["posts", "comments"]]`
5. The plan must back up every table exactly once. A table cannot be backed up until all tables it depends on (via foreign keys) have been backed up in a previous phase.
6. The `backup_scheduler` binary assigns a latency penalty for sequential phases and for unbalanced concurrent batches. You must optimize the grouping to minimize the overall simulated latency. Run `/app/backup_scheduler /home/user/backup_plan.json` to see the latency.

Your goal is to achieve a simulated latency of **less than 1500 milliseconds**.

When you are done, ensure `/home/user/backup_plan.json` contains your final optimized plan, and `/home/user/generate_plan.py` contains the code used to generate it.