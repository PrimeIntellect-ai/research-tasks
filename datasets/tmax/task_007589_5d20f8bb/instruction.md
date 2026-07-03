You are acting as a data analyst. We have three CSV files containing our raw data, and we need you to write a Go program that processes these files, performs complex aggregations (similar to a NoSQL aggregation pipeline), and outputs the results in a validated JSON format.

The CSV files are located in `/home/user/data/`:
1. `sales.csv`: `sale_id,product_id,region_id,amount,timestamp`
2. `products.csv`: `product_id,category,name,price`
3. `regions.csv`: `region_id,country,city`

Your task is to write a Go program at `/home/user/aggregate.go` that does the following:
1. Reads and parses the three CSV files.
2. Filters the `sales.csv` data to only include records where the `amount` is greater than or equal to `50.00`.
3. Performs a join-like operation to associate each sale with its corresponding product `category` and region `country`.
4. Groups the filtered sales by `category` and `country`.
5. Calculates two metrics for each group:
   - `total_revenue`: The sum of the sale `amount`s.
   - `transaction_count`: The number of sales in that group.
6. Sorts the aggregated results first by `total_revenue` in descending order, and then by `country` in ascending alphabetical order for ties.
7. Writes the final aggregated data to `/home/user/output.json`.

The output JSON must be a JSON array of objects, strictly following this schema:
```json
[
  {
    "category": "string",
    "country": "string",
    "total_revenue": 0.00, // rounded to 2 decimal places
    "transaction_count": 0
  }
]
```
Ensure your Go program is self-contained (using standard library only, if possible) and runs efficiently. You can run your code using `go run /home/user/aggregate.go` to generate the output file.

Please make sure the output file is perfectly formatted JSON and accurately reflects the aggregations.