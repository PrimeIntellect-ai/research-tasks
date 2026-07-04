You are a data engineer working on an ETL pipeline for a fintech company. A previous engineer left behind a broken pipeline that attempted to calculate the network centrality of users based on transaction data. Their SQL query had an implicit cross-join that caused massive data duplication and incorrect results. 

Your task is to build a corrected pipeline from scratch. You can use any language or standard CLI tools (like Python, `sqlite3`, `awk`, etc.) available in a standard Linux environment.

You are provided with two CSV files:
1. `/home/user/users.csv`: Contains `user_id,username,region`
2. `/home/user/transactions.csv`: Contains `tx_id,sender_id,receiver_id,amount`

You need to compute the "Degree Centrality" and "Total Volume" for each user, and then rank them within their region.

Definitions:
- **Degree Centrality**: The total number of distinct transactions a user is involved in (either as the `sender_id` or the `receiver_id`).
- **Total Volume**: The sum of the `amount` of all distinct transactions a user is involved in (either as sender or receiver). 
- **Rank**: The ranking of the user within their `region` based on Degree Centrality (highest = 1). If there is a tie in Degree Centrality, break the tie using Total Volume (highest = 1). If there is still a tie, break it alphabetically by `username` (A-Z).

Requirements:
1. Process the CSV files to calculate these metrics.
2. Use window functions (or equivalent logic) to determine the rank of each user within their region.
3. Filter the final results to only include the top 2 users per region.
4. Export the final results to a JSON file at `/home/user/top_users.json`. 

The JSON must be an array of objects, sorted by `region` (alphabetically) and then by `rank` (ascending). 
Example output format:
```json
[
  {
    "region": "EU",
    "rank": 1,
    "username": "alice",
    "degree": 5,
    "volume": 1250.0
  },
  {
    "region": "EU",
    "rank": 2,
    "username": "bob",
    "degree": 3,
    "volume": 800.0
  }
]
```
Ensure the amounts are represented as numbers, not strings. Create the output file precisely at `/home/user/top_users.json`.