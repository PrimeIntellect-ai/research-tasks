You are an ETL engineer taking over a legacy hybrid database system. The previous engineer left behind a system that stores relational data in SQLite and event logs in a simulated NoSQL document store (a folder of JSON files). 

There is a hidden relationship between the relational data and the NoSQL data, and the legacy system frequently experienced deadlocks due to circular references when querying both systems concurrently. To fix this, you need to write a standalone Python ETL script that aggregates data across both sources safely.

Your objective is to generate a summary report of VIP customers and their total completed revenue.

**Source Data:**
1. **SQLite Database:** `/home/user/etl_data/primary.db`
   * `customers` table: `id` (INT), `name` (TEXT), `signup_date` (TEXT)
   * `orders` table: `order_id` (INT), `customer_id` (INT), `amount` (DECIMAL), `status` (TEXT) - status can be 'completed', 'pending', or 'failed'.
   
2. **NoSQL JSON Store:** `/home/user/etl_data/events/`
   * A directory containing multiple JSON files. Each JSON document represents an event stream.
   * You must reverse engineer the schema to find the relationship. Hint: The documents contain nested arrays of actions. Look for an implicit reference to the customer and an action type of `"GRANT_VIP"`.

**Task:**
Write a Python script (you can name it whatever you like, e.g., `/home/user/etl.py`) that performs the following:
1. Simulates a NoSQL aggregation pipeline by parsing all JSON files in `/home/user/etl_data/events/` to find all customers who have a `"GRANT_VIP"` action in their event history.
2. Queries the SQLite database using a complex join/subquery to calculate the total `amount` of `'completed'` orders for each customer.
3. Performs a cross-query aggregation between the two datasets.
4. Outputs a CSV file at `/home/user/etl_data/vip_revenue.csv`.

**Output Format for `/home/user/etl_data/vip_revenue.csv`:**
* The CSV must have exactly two columns: `customer_name,total_revenue`
* Do not include a header row.
* Only include customers who are BOTH marked as VIP in the NoSQL events AND have a total completed revenue strictly greater than 0.
* Sort the results in descending order of `total_revenue`. If there is a tie, sort alphabetically by `customer_name`.

Ensure your Python script runs successfully and generates the exact CSV format requested.