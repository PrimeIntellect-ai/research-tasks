You are an AI assistant helping a researcher organize and analyze a recently recovered dataset. 

The researcher has a SQLite database located at `/home/user/research_data.db`. Unfortunately, the original documentation was lost, so you do not know the schema. We know it contains measurements of different plant species across various regions.

Your task is to:
1. Explore the database to understand its schema (reverse engineer the data model).
2. Write a Python script at `/home/user/analyze.py` that connects to this database and executes a single, highly-optimized SQL query (using complex joins and window functions) to extract a specific analytical report.
3. The script must output the results to a CSV file at `/home/user/top_growth.csv`.

**Report Requirements:**
For each plant, calculate the `daily_growth`, defined as the difference in height (`height_cm`) from the plant's chronologically previous measurement. 
Also, calculate the `rolling_health`, which is the average `health_score` of the current measurement and up to 2 previous measurements for that specific plant (i.e., a rolling window of size 3).
From this enriched data, find the top 2 highest `daily_growth` events per `climate_zone`. If there are ties in growth, break them by ordering `date` in ascending order.

The output CSV `/home/user/top_growth.csv` must contain exactly these columns in this order:
`climate_zone`, `species`, `date`, `daily_growth`, `rolling_health`

* `daily_growth` should be an integer.
* `rolling_health` should be a float rounded to 2 decimal places (or exactly as SQLite computes it, but ideally formatted nicely). Note: Use standard SQLite analytical functions.
* Include a header row.
* Null growths (e.g., the first measurement of a plant) should be excluded from the "top 2" rankings.

Ensure your Python script relies on SQL window functions and CTEs/subqueries to do the heavy lifting, rather than processing raw rows in Python.