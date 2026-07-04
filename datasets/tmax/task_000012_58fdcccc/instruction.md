You are assisting a climate researcher in organizing and processing a large dataset. 

The researcher has an undocumented SQLite database located at `/home/user/climate_data.db`. They wrote a Python script, `/home/user/generate_report.py`, to calculate the 3-reading moving average of temperature readings for a specific region. However, the script is incredibly slow because it loads all tables entirely into memory and performs the joins and windowing computations using nested Python loops.

Your task has three phases:
1. **Reverse Engineer Data Model & Optimize Database:** Inspect `/home/user/climate_data.db` to understand its schema. Identify the columns used for joins and filtering (specifically relating sensors, locations, and readings). Create the necessary database indexes directly in the SQLite database to optimize query execution plans for joins on sensor IDs, location IDs, and filtering by region names and sensor types.
2. **Rewrite Query & Pipeline:** Modify `/home/user/generate_report.py`. Replace the inefficient Python-level data manipulation with a single, highly optimized SQL query. The query should perform the necessary `JOIN`s, filter for sensors of type `TEMP` in the region `Alpine_Zone`, and use SQLite Window Functions (`OVER`, `PARTITION BY`) to compute the 3-reading moving average (current reading and the 2 preceding readings) directly in the database.
3. **Format Output:** The modified Python script must execute the optimized query and save the exact results to `/home/user/alpine_temp_report.json`. 

The output JSON file must strictly match this format:
```json
[
  {
    "sensor_id": 4,
    "timestamp": "2023-01-01T12:00:00",
    "value": 12.5,
    "moving_avg": 12.5
  },
  ...
]
```
Ensure that `moving_avg` is rounded to 2 decimal places. The array must be sorted by `sensor_id` ascending, then `timestamp` ascending.

Constraints:
- Do not change the database file path.
- The resulting JSON must be perfectly formatted.
- You must create at least two indexes in the database to optimize the query path.