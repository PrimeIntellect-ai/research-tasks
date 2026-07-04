You are acting as a Database Administrator optimizing an analytical pipeline. We have a localized SQLite database tracking e-commerce interactions at `/home/user/ecommerce.db`. 

Your task is to write a robust Python script at `/home/user/analyze_high_value_users.py` that takes a registration year as a command-line argument and performs a cross-query analysis to summarize high-value user behavior.

The database has the following schema:
- `users` (user_id INTEGER PRIMARY KEY, name TEXT, reg_year INTEGER)
- `orders` (order_id INTEGER PRIMARY KEY, user_id INTEGER, total NUMERIC)
- `order_items` (item_id INTEGER PRIMARY KEY, order_id INTEGER, category TEXT, price NUMERIC, quantity INTEGER)

To simulate a strict parameterized environment and prevent SQL injection, your script MUST NOT use string formatting or f-strings to insert dynamic values into SQL queries. You must strictly use SQLite parameterized queries (e.g., using `?` placeholders).

Your script must implement the following query-to-pipeline chain:
1. **Query 1:** Fetch all `user_id`s for users who registered in the year provided via the first command-line argument (`sys.argv[1]`).
2. **Query 2:** Using the fetched `user_id`s, retrieve all `order_id`s from the `orders` table where the order `total` is strictly greater than `100.00`. (You must pass the user IDs dynamically as parameters).
3. **Query 3:** Using those specific `order_id`s, query the `order_items` table to calculate the grand total sum of `price * quantity` and the total sum of `quantity` ONLY for items in the 'Electronics' category.

Finally, the script must aggregate this data and write a JSON file to `/home/user/report.json` with exactly this structure:
```json
{
  "target_year": <integer>,
  "eligible_users_count": <integer_count_of_users_from_query_1>,
  "eligible_orders_count": <integer_count_of_orders_from_query_2>,
  "total_electronics_spend": <float_sum_of_price_times_quantity>,
  "total_electronics_quantity": <integer_sum_of_quantity>
}
```
If there are no electronics items, the spend and quantity should be `0`.

Run your script for the year `2022` to generate the final report:
`python3 /home/user/analyze_high_value_users.py 2022`