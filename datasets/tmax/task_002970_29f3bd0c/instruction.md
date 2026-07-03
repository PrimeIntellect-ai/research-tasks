You are a data analyst tasked with analyzing a company's organizational chart provided as a CSV file. 

The file is located at `/home/user/employees.csv` and contains the following columns:
`emp_id`, `name`, `manager_id`, and `salary`. 

Your goal is to write a Python script that traverses this hierarchy (which forms a directed tree/graph) to extract and process the reporting chain for a specific manager.

Please write a Python script that does the following:
1. Identifies all direct and indirect subordinates of the employee with `emp_id = 2`. The employee with `emp_id = 2` should NOT be included in this subordinate list.
2. Calculates the sum total of all these subordinates' salaries.
3. Sorts the list of subordinates primarily by `salary` in descending order. If there is a tie, sort secondarily by `name` in ascending (alphabetical) order.
4. Paginates the sorted list. Assume a page size of 2 items per page. Extract exactly "Page 2" (assume 1-indexed pages, so Page 1 contains the 1st and 2nd items, Page 2 contains the 3rd and 4th items).
5. Exports the final result to a JSON file located precisely at `/home/user/org_report.json`.

The JSON file must strictly follow this structure:
```json
{
  "manager_id": 2,
  "total_subordinate_salary": <integer>,
  "page": 2,
  "page_size": 2,
  "subordinates": [
    {"emp_id": <integer>, "name": "<string>", "salary": <integer>},
    {"emp_id": <integer>, "name": "<string>", "salary": <integer>}
  ]
}
```

Ensure all numerical values in the JSON are integers. Run your script to generate the `/home/user/org_report.json` file.