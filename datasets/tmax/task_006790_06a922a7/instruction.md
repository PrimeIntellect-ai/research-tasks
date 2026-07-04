You are a data analyst dealing with a mix of legacy database dumps and flat CSV files. We had an issue with an application that caused it to write "stale" duplicated rows to our SQLite database instead of updating existing ones. 

Your task is to write a Bash script at `/home/user/run_analysis.sh` that cleans this data, joins it across formats, and outputs a properly nested JSON document.

**Input Data:**
1. An SQLite database at `/home/user/data/sales.sqlite` containing a table `order_history`:
   - `id` (INTEGER PRIMARY KEY)
   - `order_id` (INTEGER)
   - `customer_id` (INTEGER)
   - `amount` (DECIMAL)
   - `status` (TEXT) - e.g., 'PENDING', 'SHIPPED', 'CANCELLED'
   - `updated_at` (DATETIME)
   *Note: Because of the bug, there are multiple rows for the same `order_id`. The true state of an order is represented by the row with the most recent `updated_at`.*

2. A CSV file at `/home/user/data/customers.csv` containing:
   - `customer_id`
   - `first_name`
   - `last_name`
   - `region`

**Requirements for your script (`/home/user/run_analysis.sh`):**
1. You may install dependencies like `jq` or `sqlite3` if needed.
2. Use SQL window functions (e.g., via the `sqlite3` CLI) to isolate the *latest* row for each `order_id` in `order_history`.
3. Filter out any orders where the latest status is `'CANCELLED'`.
4. Join the cleaned SQLite data with the `customers.csv` data (you can import the CSV into SQLite dynamically or join via standard Bash tools).
5. Output the final aggregated data into a JSON file at `/home/user/output/active_orders.json`.

**Output Format:**
The file `/home/user/output/active_orders.json` must be a valid JSON object matching this exact structure:
```json
{
  "customers": [
    {
      "customer_id": 1,
      "full_name": "John Doe",
      "region": "North",
      "active_orders": [
        {
          "order_id": 101,
          "amount": 250.50,
          "status": "SHIPPED"
        }
      ]
    }
  ]
}
```
*Constraints for the JSON:*
- Group the data by customer.
- `full_name` should be a concatenation of `first_name` and `last_name` separated by a single space.
- Only include customers who have at least one active (non-cancelled) order.
- Sort the `customers` array by `customer_id` ascending.
- Sort the `active_orders` array within each customer by `order_id` ascending.

Make sure your script creates the `/home/user/output` directory if it doesn't exist, and write the JSON file there. Execute your script to generate the final file.