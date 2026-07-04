You are a data engineer building an ETL pipeline to extract insights from our company's internal knowledge graph.

I have placed an RDF dataset (Turtle format) at `/home/user/company_data.ttl`. This dataset contains information about employees and the projects they work on.

Your task is to write a Python script at `/home/user/etl_script.py` that queries this knowledge graph and exports an aggregated summary. You must use the `rdflib` library to parse the file and execute a SPARQL query.

The script must do the following entirely via a SPARQL query (do not do the aggregation/sorting in Python natively, let SPARQL do the work):
1. Match graph patterns to find all employees and the projects they `workOn`.
2. Aggregate the results to count the number of projects each employee works on.
3. Filter the results to only include employees working on **at least 2 projects**.
4. Sort the results first by the number of projects in **descending** order, and then by the employee's name in **ascending** (alphabetical) order.
5. Apply pagination/limiting to return only the **top 3** employees.

Finally, your Python script must export these exact SPARQL results into a JSON file at `/home/user/top_employees.json`. 

The output JSON must be a single JSON array of objects, with each object containing exactly two keys:
- `"name"` (string): The employee's name.
- `"project_count"` (integer): The number of projects they are working on.

Example of expected output format:
```json
[
  {
    "name": "John Doe",
    "project_count": 4
  },
  ...
]
```

Run your script so that `/home/user/top_employees.json` is generated successfully.