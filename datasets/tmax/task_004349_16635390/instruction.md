You are a data engineer tasked with building a high-performance graph analytics ETL query layer over a financial dataset. 

The system relies on two services:
1. A PostgreSQL database (running on `localhost:5432`, db: `etl_db`, user: `etl_user`, password: `etl_password`).
2. A Redis cache (running on `localhost:6379`).

There is a startup script `/app/start_services.sh` which launches these services and seeds the PostgreSQL database with a table named `transfers`. 
The schema is: `transfers (id SERIAL PRIMARY KEY, src INT, dst INT, amount INT, ts TIMESTAMP)`.

Your task is to write a Python command-line tool at `/home/user/query.py` that computes exact graph and window-aggregated metrics for a specific user ID. The script must be executable and accept a single integer argument `<user_id>`. It should print a single valid JSON object to standard output.

The JSON object must contain exactly these keys and compute them as follows:
- `"degree"`: An integer representing the total number of unique users this user has interacted with (either as `src` or `dst`).
- `"mutual_volume"`: An integer representing the sum of all `amount`s sent BY the user TO other users who have ALSO sent at least one transfer BACK to the user at any point in time. If none, return 0.
- `"max_rolling_3"`: An integer representing the maximum rolling sum of 3 consecutive outgoing transfers (where `src = user_id`), ordered chronologically by `ts`. If the user has fewer than 3 outgoing transfers, it is the sum of all their outgoing transfers. If they have 0 outgoing transfers, return 0.

To ensure your queries perform efficiently during the automated fuzz-testing, you must also write a SQL file at `/home/user/indexes.sql` containing `CREATE INDEX` statements. The verification environment will run this file against PostgreSQL before testing `query.py`. Your script should connect to Postgres, compute the required data, and output the exact JSON. You may use Redis to cache intermediate graph aggregations if you choose, but it is not strictly required if your Postgres queries are fast enough.

For verification, we have a compiled reference oracle at `/app/oracle_query`. Your Python script must produce bit-exact equivalent JSON output to this oracle for any user ID, and it must execute within 200ms per call.

Run `/app/start_services.sh` to initialize the environment, inspect the data, and begin developing your script.