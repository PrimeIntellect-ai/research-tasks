You are a database administrator and backend engineer. We have a locally hosted Python data API that relies on PostgreSQL and Redis, but it is currently suffering from severe performance issues and failing to properly utilize its caching layer. 

The application code is located in `/app/api.py`. There is a startup script `/app/start.sh` that initializes the database with 500,000 synthetic event logs, starts PostgreSQL, starts Redis, and launches the Flask API on port 5000.

Your tasks are:
1. **Service Gluing**: The Flask API is supposed to cache expensive aggregate summaries in Redis, but it is currently throwing connection errors or missing cache hits because the Redis configuration in `/app/api.py` is misconfigured (pointing to the wrong socket/port). Fix the Redis connection logic so it successfully caches cross-query aggregations.
2. **Query Optimization**: The endpoint `/events` accepts `user_id`, `page`, and `limit` parameters. It validates output using Pydantic, fetches the sorted paginated events, and calculates an aggregated summary of the user's total event costs. Currently, the Python code fetches all records into memory to do this, resulting in massive slowdowns. 
3. **Database Tuning**: Rewrite the SQLAlchemy/psycopg2 queries in `/app/api.py` to perform the filtering, pagination, sorting, and aggregation at the database level. Additionally, create any necessary PostgreSQL indexes in the database `app_db` (table `events`) to ensure the query executes efficiently.

To test your changes, run `/app/start.sh` to bring up the full stack. 
Ensure the API correctly serves `GET /events?user_id=<id>&page=1&limit=50`. 

An automated verification script will evaluate your solution by measuring the endpoint's response time and throughput. You must optimize the system such that the 95th percentile response time for the `/events` endpoint is strictly under 50 milliseconds.