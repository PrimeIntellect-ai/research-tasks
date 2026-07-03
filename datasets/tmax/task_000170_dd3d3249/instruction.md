You are a Database Reliability Engineer managing a backup and analytics pipeline. We have a daily process that aggregates raw activity logs from our NoSQL store (MongoDB), validates the schema, and maps it into a relational format (SQLite) for our analytics dashboard. 

Currently, the pipeline script (`/home/user/backup_mapper.py`) is broken. It suffers from three major issues:
1. **Inefficient Aggregation:** The MongoDB aggregation pipeline is incredibly slow. It needs an index, and the pipeline itself needs to be optimized.
2. **Schema Validation Missing:** The output from MongoDB is not being validated before insertion. We need to enforce a strict schema using Pydantic.
3. **Deadlocks:** The script attempts to write to the SQLite database using multiple threads to speed up inserts, but it frequently deadlocks due to concurrent transaction contention.

Your task is to fix this pipeline end-to-end.

**Initial Setup:**
1. You must install necessary dependencies: `pymongo`, `pydantic`.
2. Start a local MongoDB instance in the background. Create a directory `/home/user/mongo_data` and start MongoDB using `mongod --dbpath /home/user/mongo_data --fork --logpath /home/user/mongod.log`.
3. Seed the MongoDB database `analytics_db`, collection `activity_logs`, using the file `/home/user/seed.json` (you will need to write a quick script or use `mongoimport` to load this array of JSON objects).

**Fixing the Pipeline (`/home/user/backup_mapper.py`):**
1. **Query Plan & Optimization:** Create an index on `activity_logs` to optimize the grouping operation by `user_id`. Write a script `/home/user/explain_plan.py` that runs `.explain("executionStats")` on your optimized aggregation pipeline and writes the JSON string output to `/home/user/query_plan.json`.
2. **Schema Validation:** In `backup_mapper.py`, create a Pydantic model named `UserStats` with fields: `user_id` (str), `total_actions` (int), and `latest_action_date` (str, ISO format). Validate every aggregated document through this model. Filter out any documents that fail validation (do not insert them).
3. **Cross-Representation Mapping:** The SQLite database `/home/user/analytics.db` has a table `user_summary` (columns: `user_id TEXT PRIMARY KEY`, `total_actions INTEGER`, `latest_action_date TEXT`). Map your validated Pydantic models to this table.
4. **Fix the Deadlock:** Modify the SQLite insertion logic in `backup_mapper.py`. You must process the inserts efficiently without causing an SQLite `OperationalError: database is locked` or a deadlock. You may refactor the threading completely, use batching, or serialize the database writes—whatever ensures reliability while successfully importing all valid data.

**Execution:**
Run your fixed `/home/user/backup_mapper.py`. It should complete successfully and populate `/home/user/analytics.db`. 

**Final Expected State:**
- `/home/user/analytics.db` exists and contains exactly the validated, aggregated records.
- `/home/user/query_plan.json` exists and contains the MongoDB explain plan for the aggregation.
- The pipeline script executes cleanly without deadlocks.