You are a database administrator tasked with optimizing a data extraction process for a poorly documented NoSQL database backup. The backup consists of several JSON Lines (JSONL) files, and you need to reverse-engineer the schema relationships to generate a specific aggregated report.

You are provided with three data files in `/home/user/data/`:
1. `users.jsonl`
2. `products.jsonl`
3. `orders.jsonl`

Your task is to write a Python script at `/home/user/aggregate.py` that reads these files and generates a summary report of top customers based on specific criteria. The output must be saved to `/home/user/report.json` and must conform exactly to a JSON schema provided at `/home/user/schema.json`.

The report must contain a JSON array of users who meet the following conditions:
1. The user must have placed at least one order with the status `"completed"`.
2. Within those completed orders, the user must have purchased at least one product belonging to the `"Electronics"` category.

For the users that meet these criteria, you need to calculate:
- `total_spent`: The total amount of money spent across ALL of their `"completed"` orders (including non-electronics items). The price of an item is in the products data, and the quantity is in the orders data.
- `electronics_purchased`: A deduplicated list of the names of the `"Electronics"` products they purchased in completed orders, sorted alphabetically.

The final JSON array in `/home/user/report.json` must be sorted by `total_spent` in descending order. If there is a tie, sort by the user's name in alphabetical order.

You need to figure out the exact field names and how the collections relate to each other by inspecting the JSONL files. Ensure your final output strictly validates against `/home/user/schema.json`. You can install any Python libraries you need, but you must not rely on an external database server (process the files directly in Python).