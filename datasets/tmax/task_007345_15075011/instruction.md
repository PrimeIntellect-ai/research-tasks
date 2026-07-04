You are an ETL data engineer tasked with building a pipeline to extract, transform, and analyze employee communication data from an undocumented legacy system.

There is a SQLite database located at `/home/user/etl/source.db` containing tables with obfuscated names. Your task is to:
1. Reverse-engineer the data model by inspecting the tables. You will find a table of departments, a table of employees (linked to departments), and a table of messages between employees.
2. Build a Python script at `/home/user/etl/pipeline.py` that extracts this data.
3. Use the extracted data to build a directed graph where nodes are employees and edges represent a message sent from one employee to another. 
4. Calculate the In-Degree Centrality for each employee (using `networkx` or writing the algorithm manually). In-degree centrality here should be defined simply as the number of incoming edges divided by `(N-1)`, where `N` is the total number of employees in the entire graph. Multiple messages from the same sender to the same receiver should count as a single edge (unweighted graph).
5. Perform cross-query aggregation to calculate the average In-Degree Centrality for each department.
6. Filter out any departments that have strictly fewer than 2 employees.
7. Sort the remaining departments by their average in-degree centrality in descending order. For ties, sort alphabetically by department name.
8. Within each department, paginate/filter the employees to include only the Top 2 employees by their individual in-degree centrality (descending). Break ties alphabetically by employee name.
9. Write the final structured data to `/home/user/etl/output/dept_summary.json`.

The output JSON must strictly match this structure:
```json
[
  {
    "department_name": "Engineering",
    "average_centrality": 0.25,
    "top_employees": [
      {
        "name": "Alice",
        "centrality": 0.4
      },
      {
        "name": "Bob",
        "centrality": 0.2
      }
    ]
  }
]
```

Constraints:
- Float values should be rounded to 4 decimal places.
- Create the `/home/user/etl/output/` directory if it does not exist.
- You may install `networkx` or any other library using `pip` if needed.
- Execute your script so that the JSON file is generated.