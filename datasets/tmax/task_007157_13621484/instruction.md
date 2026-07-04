You are an AI assistant helping a climate researcher organize and extract data from a large, unoptimized SQLite database. 

The researcher has a database at `/home/user/research.db` containing four tables:
1. `locations` (id, name, region)
2. `researchers` (id, name, department)
3. `samples` (id, location_id, researcher_id, collection_date, type)
4. `measurements` (id, sample_id, metric_name, value)

Your task is to optimize the database and write a Python script to extract a very specific, paginated subset of data.

**Requirements:**

1. **Database Optimization:**
   Analyze the schema and create the necessary SQL indexes in `/home/user/research.db` to optimize the query described below. The query should use indexes for filtering and joining, avoiding large full table scans.

2. **Query Construction & Extraction:**
   Write a Python script at `/home/user/extract.py` that connects to the database and performs the following query:
   - Find samples of type `'ice_core'` located in the `'Polar'` region.
   - For these samples, we only care about the `'carbon_ppm'` metric.
   - Calculate the maximum `'carbon_ppm'` measurement for each of these samples.
   - The result row should contain: `sample_id`, `location_name`, `researcher_name`, `collection_date`, and `max_carbon`.
   - Order the results primarily by `max_carbon` descending, and secondarily by `collection_date` ascending.
   - Apply pagination: Retrieve exactly **Page 2**, where each page contains exactly **15** records (i.e., you need records 16 through 30).

3. **Outputs:**
   Your Python script (`/home/user/extract.py`) must do the following when executed:
   - Execute the query and save the fetched results as a JSON array of objects to `/home/user/results.json`. Each object should have the keys: `sample_id`, `location_name`, `researcher_name`, `collection_date`, `max_carbon`.
   - Prepend `EXPLAIN QUERY PLAN` to your exact SQL query string, execute it, and write the raw string output of the query plan to `/home/user/plan.txt`.

Ensure your Python script runs cleanly without errors.