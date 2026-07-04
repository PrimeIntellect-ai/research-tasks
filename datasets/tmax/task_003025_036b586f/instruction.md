You are a database administrator tasked with optimizing a background worker system that is currently experiencing severe performance degradation.

In the `/app` directory, there is a multi-service setup consisting of a local Redis instance and a Python background processing system. 
The system works as follows:
1. Redis is running locally on port 6379.
2. A producer script (`/app/producer.py`) has already populated a Redis List called `job_queue` with 500 user IDs.
3. A consumer script (`/app/consumer.py`) pops these IDs from Redis, queries a large SQLite database (`/app/logs.db`) to aggregate the total `duration` of all `video_play` actions for each user, and exports the final aggregated data to `/app/results.json`.

Currently, `consumer.py` takes far too long to execute because the SQLite database schema is poorly optimized for the query being executed, and the consumer relies on inefficient query plans.

Your tasks:
1. Reverse engineer the data model of `/app/logs.db`.
2. Design and implement an optimal indexing strategy in the SQLite database to dramatically speed up the specific queries run by `consumer.py`. You may modify the database schema (e.g., add indexes) using the `sqlite3` CLI.
3. Review and optimize the SQL query inside `/app/consumer.py` if necessary, ensuring it leverages your new index using `EXPLAIN QUERY PLAN` principles.
4. Run `/app/consumer.py` so that it completely processes the queue and successfully generates `/app/results.json`.
5. The final `results.json` must be a key-value dictionary mapping the user ID (as a string) to the total duration (as an integer).

Your optimization will be verified by an automated performance test. The execution time of your consumer script processing the 500 jobs must be significantly reduced.