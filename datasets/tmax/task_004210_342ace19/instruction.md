You are an expert data engineer. We have an existing ETL pipeline script at `/app/etl.py` that is supposed to aggregate employee data, but it is currently producing massively inflated and incorrect results due to a bad SQL query. Additionally, it lacks the integration of event logs and department mappings.

Here is what you need to do:

1. **Fix the SQL Query**:
   The script reads from `/app/data.db`. The current query in `etl.py` has an implicit cross join that causes a massive explosion of rows. Fix the SQL query to correctly join `employees`, `departments`, and `employee_departments`. 
   Update the query to also include a window function that calculates each employee's salary rank (`salary_rank`) within their department (highest salary = rank 1).

2. **Extract Department Mappings**:
   There is an image file at `/app/schema_clue.png` containing a critical department ID to name mapping that was lost during a migration. Use OCR (e.g., `tesseract`) to extract this mapping. The image contains text in the format `MAPPING: { "D1": "Engineering", ... }`. 

3. **NoSQL Aggregation**:
   Parse the JSON lines file at `/app/events.json`. Perform an aggregation to count the number of login events (`event_type: "login"`) per employee ID.

4. **Serve the Data**:
   Modify the Python script to run an HTTP server using `Flask` or `http.server` on `127.0.0.1:8080`.
   The server must expose a `GET /api/employees` endpoint.
   The endpoint should return a JSON array of objects, where each object represents an employee and contains:
   - `employee_id`: The employee's ID.
   - `name`: Employee's name.
   - `department_name`: The mapped department name extracted from the image.
   - `salary_rank`: Integer rank within the department.
   - `login_count`: Integer count of login events from the JSON file.

Ensure your server remains running so it can be queried. The response should be sorted by `employee_id` ascending.