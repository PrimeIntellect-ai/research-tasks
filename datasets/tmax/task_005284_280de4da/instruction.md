You are a data engineer building an ETL pipeline to process human resources data. 

You have been provided with an organizational chart in a CSV file located at `/home/user/employees.csv`.
The CSV has the following schema (including a header row):
`ID,Name,ManagerID,Role`

Your task is to write a bash script, or run shell commands, to compute the "management depth" of every employee in the company. The "depth" is defined hierarchically:
- An employee with no `ManagerID` (empty) is at the root of the hierarchy and has a depth of `0`.
- An employee's depth is exactly `1 + (their manager's depth)`.

You must project this hierarchical relationship and export the final results into a properly formatted JSON array file at `/home/user/hierarchy.json`.

The JSON file must be an array of objects, sorted numerically by the employee's `ID` in ascending order. Each object must strictly have the following format:
```json
[
  {
    "id": 1,
    "name": "Alice",
    "depth": 0
  },
  ...
]
```

Requirements:
1. Parse the CSV file and handle the hierarchical projection (recursive mapping) to find each employee's depth.
2. Format the output as valid JSON.
3. Save the final JSON array exactly at `/home/user/hierarchy.json`.
4. Ensure the output is valid JSON (it will be parsed by `jq` during verification) and correctly calculates depths for all employees in the dataset.