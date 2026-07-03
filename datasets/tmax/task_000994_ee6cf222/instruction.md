You are acting as a Data Engineer. We have a set of relational CSV files containing e-commerce data that we need to denormalize and export into a NoSQL-compatible JSONL format (one JSON object per line).

You have been provided with two CSV files:
1. `/home/user/data/customers.csv`
2. `/home/user/data/orders.csv`

Additionally, there is an image file located at `/app/business_rules.png` that contains a specific formula for calculating a `customer_value_score`. You will need to extract this formula (e.g., using OCR with `tesseract` or by writing a quick vision script) and apply it to the data.

Your objective:
1. Read and parse the CSV files.
2. Group the orders by customer to calculate:
   - `total_spent`: The sum of `total_amount` for all orders belonging to the customer.
   - `order_count`: The total number of orders the customer has placed.
   - `days_since_last_order`: The number of days between the customer's most recent `order_date` and the reference date of **'2023-12-31'**.
3. Calculate the `customer_value_score` based on the formula extracted from `/app/business_rules.png`.
4. Export the resulting data to a JSONL file at `/home/user/customers_export.jsonl`. 

Each line in the JSONL file must validate against this structure:
- `_id` (integer): The `customer_id`
- `total_spent` (float): Sum of total_amount
- `order_count` (integer): Total number of orders
- `days_since_last_order` (integer): Days since most recent order to '2023-12-31'
- `customer_value_score` (float): The score calculated from the formula in the image.

You can use Python, Node.js, or shell tools to accomplish this. Tesseract OCR is installed if you need it. 

Your final output file `/home/user/customers_export.jsonl` will be evaluated automatically by comparing your calculated `customer_value_score` values against a hidden reference implementation using Mean Squared Error (MSE). You must achieve an MSE of less than 0.1.