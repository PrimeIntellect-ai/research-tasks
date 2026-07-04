I am a developer debugging a failing build for our backend data pipeline. The pipeline involves a Flask application, a Redis cache, and a SQLite database. The integration tests are failing, and I need you to fix the system.

Here are the issues you need to resolve:

1. **Legacy Binary Migration**: We are migrating a legacy C utility to Python to improve maintainability. The legacy stripped binary is located at `/app/legacy_processor.bin`. It takes a single string as a command-line argument and prints a processed string to standard output. 
   You must reverse-engineer this binary and write a bit-exact equivalent Python script at `/home/user/processor.py`. Your script should accept the string as `sys.argv[1]` and print the result. The automated test will fuzz-test your Python script against the legacy binary using thousands of random strings to ensure identical behavior.

2. **Database Recovery**: The SQLite database at `/app/metrics.db` has been corrupted during a power failure, but its Write-Ahead Log (WAL) at `/app/metrics.db-wal` is intact. You need to recover the database so that it can be queried normally. Ensure the recovered database is placed at `/app/metrics_recovered.db`.

3. **Recursion Bug**: The Flask application at `/app/app.py` has a logical bug in the `compute_recursive_metric` function that causes a `RecursionError` when hitting the `/process` endpoint. You need to identify and fix the loop/recursion termination condition in this function. Add assertions to the function to validate the inputs intermediate states.

4. **Service Orchestration**: You must bring up the services for end-to-end testing. 
   - Start a Redis server on the default port (6379).
   - Start the Flask app on port 5000.
   - The Flask app requires the environment variables `REDIS_URL=redis://localhost:6379/0` and `DB_PATH=/app/metrics_recovered.db`.

Once you have fixed the code, recovered the database, and started the services, let me know. An automated test will verify the fuzz-equivalence of your script and execute an end-to-end protocol flow against the Flask API.