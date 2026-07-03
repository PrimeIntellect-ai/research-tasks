You are a data analyst tasked with processing a messy CSV dump from our IoT sensors and setting up an automated analysis pipeline using C++ and MongoDB. 

The raw data is located at `/home/user/sensor_dump.csv`. The file contains append-only sensor readings, meaning there are multiple rows for the same sensor (representing different points in time), and some rows contain stale or corrupted data flagged by the system.

You need to write a C++ program at `/home/user/analyze.cpp` that performs the following tasks when compiled and executed:

1. **Reverse Engineer the Data Model**: Inspect the CSV to understand its structure. 
2. **Data Import**: Your C++ program must programmatically invoke a shell command to import this CSV into a local MongoDB instance (database: `iot`, collection: `readings`). Assume MongoDB is already installed and running on default ports without authentication.
3. **NoSQL Aggregation Pipeline**: Construct a MongoDB aggregation pipeline that:
   - Filters out any rows where the status is explicitly marked as corrupted/error.
   - For each unique sensor, isolates the most recent valid reading (based on the timestamp).
   - Groups these latest readings by location and calculates the average temperature for each location.
4. **Query Execution & Optimization Plan**: 
   - Your C++ program must execute this pipeline using `mongosh` (via `system()` or `popen()`) and write the final aggregated result (in JSON format) to `/home/user/final_report.json`.
   - Your program must also run an `explain("executionStats")` on the pipeline to interpret the query plan, saving the explain output to `/home/user/query_plan.json`.
5. **Index Creation**: To optimize this pipeline, your C++ program must first create an appropriate index in the MongoDB collection that specifically targets the filtering and sorting stages of your pipeline.

**Requirements:**
- Compile your C++ code to `/home/user/analyze` (e.g., `g++ /home/user/analyze.cpp -o /home/user/analyze`).
- We will run `/home/user/analyze` to verify your solution.
- Do not use third-party C++ libraries (like `mongocxx`) to avoid complex dependency management; instead, construct the `mongoimport` and `mongosh` commands as strings within your C++ code and execute them via the standard `<cstdlib>` system functions.
- The final JSON report `/home/user/final_report.json` must clearly show the locations and their average temperatures.