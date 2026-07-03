You are assisting a research team in organizing their dataset infrastructure. They have an SQLite database at `/home/user/app/data/research.db` that continuously receives sensor measurements from a background Python service (`/home/user/app/ingestor.py`). 

Recently, the researchers noticed two critical issues:
1. Queries filtering or ordering by timestamp are returning stale or missing rows. The database has a corrupted index named `idx_time` on the `measurements` table.
2. They need a fast, real-time analytical API to query cumulative rolling averages of the sensor data, but the current C++ query server is incomplete.

Your objectives are:
1. **Repair the Database**: Fix the corrupted `idx_time` index in `/home/user/app/data/research.db` without losing any data.
2. **Implement the Analytics Endpoint**: Complete the C++ server source code at `/home/user/app/server/main.cpp`. The server must use the provided `cpp-httplib` (header at `/home/user/app/server/httplib.h`) and `sqlite3` to serve HTTP requests.
3. **Endpoint Specification**:
   - Route: `GET /api/v1/stats`
   - Query Parameter: `exp_id` (integer)
   - Behavior: Retrieve all measurements for the given `exp_id`, ordered by `timestamp` ascending.
   - Analytics: Use a SQL window function to calculate the `cumulative_avg` of `sensor_value` up to that row (partitioned by `exp_id` and ordered by `timestamp`).
   - Response Format (JSON):
     ```json
     {
       "schema_version": "1.0",
       "data": [
         {
           "id": 1,
           "timestamp": "2023-10-01T10:00:00Z",
           "sensor_value": 10.5,
           "cumulative_avg": 10.5
         }
       ]
     }
     ```
4. **Service Composition**: 
   - Start the data ingestor: `python3 /home/user/app/ingestor.py &`
   - Compile the C++ server: `g++ -std=c++17 main.cpp -lsqlite3 -lpthread -o server` (inside `/home/user/app/server/`)
   - Start the C++ server so it listens on `127.0.0.1:8080`.

Ensure both services are running and that the C++ server correctly queries the updated database. Do not change the schema of the tables. The `measurements` table has columns `id`, `exp_id`, `timestamp`, and `sensor_value`.