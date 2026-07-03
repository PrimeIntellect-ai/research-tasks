You are a data analyst troubleshooting a reporting pipeline. 

In your home directory (`/home/user`), there is an RDF dataset named `data.ttl` containing information about employees, their salaries, and the departments they work in. 

There is also a Python script named `report.py` that uses the `rdflib` library to query this data using SPARQL. Currently, the script produces incorrect, exploded results. This is because the SPARQL query contains an implicit cross-join—it retrieves all employees and all departments without correctly linking them together based on their relationships in the graph.

Your task is to fix the script and implement several new reporting features:

1. **Fix the Cross-Join:** Correct the SPARQL query so that it properly links employees to their respective departments using the graph's structure.
2. **Analytical Aggregation:** Modify the query to group the data by department and calculate the average salary for each department.
3. **Parameterization:** The script defines a `MIN_SALARY` variable. You must inject this into the SPARQL execution securely (using parameterized query bindings in `rdflib`, i.e., passing `initBindings`, rather than using insecure string formatting). Only employees with a salary strictly greater than this threshold should be included in the average.
4. **Sorting and Pagination:** Order the final aggregated results by the average salary in descending order. Apply pagination directly in the SPARQL query to return only the top 2 departments (Limit 2).
5. **Output:** The script must write the final results to `/home/user/summary.csv`. The CSV must have exactly two columns: `DepartmentName` and `AverageSalary`. Do not include a header row. Format the average salary as an integer (e.g., `100000`).

You may install any standard Python packages you need using `pip`, though `rdflib` should be sufficient. Run your fixed script to generate the final `summary.csv`.