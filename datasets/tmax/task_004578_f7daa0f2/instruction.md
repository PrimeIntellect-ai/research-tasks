You are acting as a data analyst. I have three CSV files representing a mock social payment network. I need you to write a Go program to process these files, perform several analytical aggregations and graph operations, and output a specific paginated JSON result. 

The three input files are located at:
1. `/home/user/users.csv` - Columns: `user_id`, `name`
2. `/home/user/friends.csv` - Columns: `source_id`, `target_id` (representing a directed friendship from source to target)
3. `/home/user/transactions.csv` - Columns: `tx_id`, `user_id`, `amount`, `timestamp`

Write a Go program at `/home/user/process.go` that does the following:

1. **Graph Analytics (Centrality):** Calculate the out-degree centrality for each user. This is defined as the total number of outbound friendships (where the user is the `source_id`) in `friends.csv`.
2. **Analytical Aggregation (Window-like):** For each user, find their highest single transaction `amount` from `transactions.csv`. If a user has no transactions, their max transaction amount is 0.0.
3. **Join and Filter:** Combine the user's details (`user_id`, `name`), out-degree centrality, and max transaction amount. Filter the results to keep ONLY users whose max transaction amount is **strictly greater than** 50.0.
4. **Sort:** Sort the filtered results using the following priority:
   - Max transaction amount (Descending)
   - Out-degree centrality (Descending)
   - User ID (Ascending)
5. **Pagination:** Apply pagination to the sorted results. Assuming a page size of 2, extract **Page 2** (where Page 1 is the first 2 items, so Page 2 contains the 3rd and 4th items in the sorted list).
6. **Output:** Write the paginated result as a JSON array to `/home/user/output.json`. The JSON objects should exactly match this structure:
```json
[
  {
    "user_id": 123,
    "name": "John Doe",
    "out_degree": 4,
    "max_amount": 105.50
  }
]
```

Requirements:
- Ensure amounts are formatted as JSON numbers (floats).
- Use standard Go libraries (e.g., `encoding/csv`, `encoding/json`, `sort`). You do not need to use an external database or third-party packages, but you can process the data in-memory using Go structs and maps.
- Compile and run your Go program to generate the `/home/user/output.json` file.