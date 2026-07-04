You are an expert data analyst and engineer. We have a multi-service data pipeline that processes supply chain routes. 

Our system consists of two microservices running locally:
1. **Ingestion API** (Port 5000): Receives CSV data and writes it to an SQLite database (`/app/data/routes.db`).
2. **Query API** (Port 5001): Computes shortest paths for the supply chain network using the database.

**The Problem:**
Recently, a massive new CSV file (`/app/data/new_routes.csv`) was loaded via the Ingestion API. However, the Query API is returning stale data (it does not reflect the new routes) and its performance has degraded significantly. We suspect the Query API is reading from a stale materialized cache table (`routes_cache`) instead of executing a live recursive query on the `routes` table, and the underlying database lacks the proper indexes for efficient graph traversal.

**Your Tasks:**
1. **Service Reconfiguration:** Inspect and modify the Query API source code (`/app/query_api/app.py`). Update it to bypass the stale `routes_cache` table and instead perform a live graph traversal using a Recursive Common Table Expression (CTE) to find the shortest path from a given `source` to a `destination`.
2. **Database Optimization:** The recursive CTE will be too slow on the raw `routes` table. Analyze the query plan and apply necessary database optimizations (e.g., creating specific indexes) directly to `/app/data/routes.db` to drastically reduce execution time.
3. **Data Analysis Script:** Write a Python script at `/home/user/analyze.py` that interacts with the fixed Query API. Your script must:
    - Query the API for shortest paths from node `WH_ALPHA` to all other nodes starting with `STORE_`.
    - Retrieve the path lengths (total cost).
    - Use Python to compute a windowed analytical aggregation: Rank the destinations by their shortest path total cost in ascending order (Rank 1 = lowest cost).
    - Save the final results as a JSON file at `/home/user/results.json` in the following format:
      ```json
      [
        {"destination": "STORE_102", "total_cost": 45.5, "rank": 1},
        {"destination": "STORE_055", "total_cost": 48.0, "rank": 2}
      ]
      ```

**Constraints:**
- You must use bash tools and Python.
- Do not modify the Ingestion API.
- Your `analyze.py` script must be highly performant. The automated verification system will strictly measure its end-to-end execution time. It must complete in under 2.0 seconds. 
- You must restart the Query API service after modifying it to ensure changes take effect. The services are managed via `systemctl --user restart query-api` (or similar, depending on the exact setup you find in `/app/`).