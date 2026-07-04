You are acting as a Database Administrator for our company. We have an SQLite database located at `/home/user/company.db` containing two tables:

1. `org_chart` - Represents our employee hierarchy (Graph).
   - `emp_id` (INTEGER): The employee's ID.
   - `manager_id` (INTEGER): The ID of the employee's manager (NULL if they are the CEO).

2. `events` - Stores raw event logs (NoSQL document style).
   - `event_id` (INTEGER): Unique event ID.
   - `emp_id` (INTEGER): The employee who triggered the event.
   - `payload` (TEXT): A JSON string containing event details. Example: `{"type": "sale", "amount": 250, "timestamp": "2023-10-01T14:30:00"}`

Your task is to write a SQL query (saved to `/home/user/query.sql`) and execute it to produce a CSV report at `/home/user/report.csv`. 

The report must do the following:
1. **Graph Projection**: Traverse the `org_chart` to find employee ID `1` (the VP of Sales) and *all* of their direct and indirect subordinates (the entire subtree).
2. **NoSQL Aggregation**: For this specific subset of employees, query the `events` table and extract the `amount` and `timestamp` from the JSON `payload`, but *only* for events where the JSON `type` is exactly `"sale"`.
3. **Window Functions**: Calculate the cumulative sum of the sale `amount` for each employee over time (ordered by `timestamp` ascending). 
4. **Output Specifications**: 
   - The CSV must include headers exactly as follows: `emp_id,event_timestamp,sale_amount,cumulative_sales`
   - Sort the final result by `emp_id` ASC, then by `event_timestamp` ASC.
   - Export the results to `/home/user/report.csv`.

You can use standard SQLite JSON functions, Window functions, and Recursive CTEs. Please execute your script to generate the final CSV file.