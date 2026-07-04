You are a data engineer tasked with building an ETL pipeline step that extracts specific hierarchical metrics from an undocumented SQLite database. 

You have been provided with an SQLite database file at `/home/user/company.db`. The schema is completely unknown to you. Your task is to:

1. **Reverse Engineer the Schema**: Inspect the database to find the tables. There is an employee table (which contains a self-referencing foreign key denoting the manager-subordinate relationship) and a department table.
2. **Graph/Hierarchical Analysis**: Write queries/scripts to calculate the total number of *descendants* (both direct and indirect reports) for every employee in the company tree.
3. **Filter & Join**: Identify the single employee belonging to the 'Engineering' department who has the *highest* total number of descendants.
4. **Export and Format Conversion**: Once you identify this top Engineering manager, calculate their management chain upwards to the absolute root of the company (the employee with no manager). Export your findings to a strictly formatted JSON file at `/home/user/eng_top_mgr_hierarchy.json`.

The JSON file must have exactly the following structure:
```json
{
  "target_employee": "Employee Name",
  "department": "Engineering",
  "descendant_count": 0,
  "chain_to_ceo": ["Root Employee Name", "Intermediate Manager Name", "Target Employee Name"]
}
```
*Note: `chain_to_ceo` must be an ordered list of names starting from the absolute top-level manager (the CEO) down to the target employee.*

You may use Bash, Python, or standard SQLite CLI commands to complete this task. Create the required JSON file once you are done.