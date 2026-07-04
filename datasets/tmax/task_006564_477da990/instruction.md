You are a database administrator tasked with optimizing a data extraction pipeline from a legacy semantic web graph into a new application format. 

We have an organizational graph database exported as an RDF Turtle file at `/home/user/org.ttl`. It contains data about employees, the departments they belong to, their tenure (in years), and who they manage. 

Your task is to write a Python script at `/home/user/pipeline.py` that processes this data. Your script must perform the following steps:

1. **Graph Querying**: Use the `rdflib` library (you may need to install it) to load `/home/user/org.ttl` and execute a SPARQL query that extracts every employee's name, department name, tenure, and the names of the employees they directly manage. 
2. **Aggregation Pipeline**: Pass the SPARQL query results into a NoSQL-style data transformation pipeline in Python to:
   - Identify "Key Managers": filter the employees to keep ONLY those who directly manage **2 or more** people.
   - Group these Key Managers by their department.
   - Calculate the average tenure of these Key Managers for each department.
3. **Sorting & Pagination**: 
   - Sort the resulting grouped data by the average tenure in strictly descending order. If there is a tie, sort alphabetically by department name.
   - Apply pagination to retrieve exactly the first "page" of results, where a page consists of exactly 2 records (i.e., offset 0, limit 2).
4. **Output**: Save the paginated result as a JSON array to `/home/user/result.json`.

The resulting JSON must strictly match this format:
```json
[
  {
    "department": "DepartmentName",
    "avg_tenure": 10.5
  },
  ...
]
```

Constraints:
- You must use SPARQL to query the initial graph relationships.
- You must write the output exactly to `/home/user/result.json`.
- Run your script to ensure the JSON file is generated successfully before finishing.