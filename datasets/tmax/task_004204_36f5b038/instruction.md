You are a data analyst tasked with processing an organization's reporting structure to calculate budget allocations. You have been provided with two CSV files representing a directed graph of employees:

1. `/home/user/nodes.csv`: Contains employee information.
   Columns: `id,name,department,budget`
2. `/home/user/edges.csv`: Contains the reporting hierarchy (directed edges from manager to subordinate).
   Columns: `source,target`

Your objective is to write a script (in Python or Bash) to perform the following graph aggregations:
1. Identify all "Director" nodes. A Director is defined as an employee who has an in-degree of exactly 0 (they report to no one) and an out-degree of at least 1 (they manage at least one person).
2. For each Director, calculate their "Network Budget". The Network Budget is the sum of the `budget` of the Director themselves, plus the `budget` of all employees reporting to them up to exactly 2 hops away (i.e., their direct reports, and the direct reports of their direct reports).
3. Output the results to a JSON file located at `/home/user/director_budgets.json`. The JSON should be a single dictionary mapping the Director's `name` to their calculated integer Network Budget.

Example output format for `/home/user/director_budgets.json`:
```json
{
  "Alice": 240,
  "Bob": 150
}
```

You may use standard libraries available in Python or standard Linux shell tools. Do not install any external dependencies. Ensure your script strictly follows the up-to-2-hops rule for the budget aggregation.