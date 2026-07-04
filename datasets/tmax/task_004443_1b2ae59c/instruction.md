You are a data analyst tasked with processing e-commerce CSV files and building a reporting tool. 

You have been given two CSV files in `/home/user/data/`:
1. `products.csv` (Columns: `product_id`, `category`, `name`)
2. `sales.csv` (Columns: `transaction_id`, `date`, `product_id`, `quantity`, `price`)

Your task is to write a robust Bash script located at `/home/user/generate_report.sh` that takes two arguments:
1. `category` (string, e.g., "Electronics")
2. `page` (integer, 1-indexed, e.g., 2)

The script must perform the following:
1. Join the sales and products data.
2. Calculate the total revenue (`quantity * price`) for each product.
3. Compute the rank of each product within its `category` based on total revenue in descending order. Use standard competition ranking (1, 2, 2, 4) for ties.
4. Filter the results to only include the specified `category`.
5. Sort the results primarily by `rank` (ascending) and secondarily by `product_id` (ascending) to ensure deterministic ordering.
6. Paginate the results for the requested `page`, where each page contains exactly **2 items**.
7. Output the paginated result to standard output strictly as a formatted JSON document.

The output JSON must map the relational data into a document structure like this:
```json
{
  "category": "RequestedCategory",
  "page": 2,
  "results": [
    {
      "rank": 3,
      "product_id": 5,
      "name": "Shirt",
      "total_revenue": 200
    },
    ...
  ]
}
```

Constraints:
- You must write the main logic in `/home/user/generate_report.sh`.
- The script must be executable.
- You can use any commonly available Linux tools (e.g., `sqlite3`, `jq`, `python3`, `awk`) within your bash script.
- Ensure ties are handled correctly with standard competition ranking, and pagination breaks ties via `product_id`.

To verify your solution, the automated test will run commands like `./generate_report.sh Clothing 2` and check the JSON output.