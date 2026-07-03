You are a Data Engineer building an ETL pipeline to materialize a graph projection from an internal microservice into a flat analytical file.

Our company's organizational data is exposed via a paginated JSON HTTP API. You need to extract this data, load it into a relational database, and compute the "Total Reporting Salary" for every employee. The Total Reporting Salary is defined as the employee's own salary plus the salaries of all their direct and indirect reports (the entire subtree under them in the organizational hierarchy).

System Architecture & Setup:
- A PostgreSQL database server and a Python Flask API are provided.
- You must start the services by running `/app/start_services.sh`. 
- The API will be available at `http://localhost:5000/api/employees?page=1`.
- PostgreSQL will be running on localhost:5432 (user: `postgres`, no password).

API Details:
- The endpoint returns JSON in this format: 
  `{"data": [{"id": 1, "manager_id": null, "salary": 100000}, ...], "next_page": 2}`
- If `next_page` is `null`, you have reached the end.
- `manager_id` is the `id` of the employee's manager (forming a tree). The root has `manager_id: null`.

Your task:
1. Extract all employee data from the API using shell utilities (e.g., `curl`, `jq`).
2. Load the data into a PostgreSQL database named `org_db`.
3. Write and execute an optimized Recursive CTE (or similar graph projection) to calculate the Total Reporting Salary for every employee.
4. Export the final results to `/home/user/total_salaries.csv`. The CSV must have exactly two columns: `id` and `total_salary`, sorted by `id` ascending. It should not contain a header row.

Your entire workflow should be encapsulated in a shell script at `/home/user/etl.sh` that performs the extraction, DB loading, and CSV export. Once your script is ready, run it to generate the final CSV. 

We will verify your work by comparing your CSV to the ground truth. Your accuracy must be 1.0 (100% correct).