You are acting as a Database Administrator and Go Developer. 

We have a social network graph stored in a SQLite database at `/home/user/graph.db`. The database has a single table `edges(source_id INTEGER, target_id INTEGER)` representing bidirectional friendships.

There is a Go script at `/home/user/analyze.go` that is supposed to generate "Friend Recommendations" using a graph pattern matching SQL query. However, the current SQL query contains a severe bug (an implicit cross join) that causes it to return incorrect results and run inefficiently.

Your task is to fix the SQL query in `/home/user/analyze.go` and ensure the script produces the correct output. 

The correct query must:
1. Find pairs of users (`user1`, `user2`) who are NOT currently friends (no direct edge exists between them).
2. Ensure they share at least one mutual friend (an intermediate node they both have an edge to).
3. To avoid duplicate pairs, strictly enforce `user1 < user2`.
4. Count the number of `mutual_friends` they share.
5. Use a SQL Window Function to assign a `rank` to each pair. The rank must be computed by ordering the pairs by `mutual_friends` descending, then by `user1` ascending, and finally by `user2` ascending.
6. Return only the top 10 recommended pairs based on the rank.

The Go script must execute this query and save the exact output to `/home/user/recommendations.json` as a JSON array of objects with the following structure:
```json
[
  {
    "user1": 1,
    "user2": 6,
    "mutual_friends": 4,
    "rank": 1
  }
]
```

Requirements:
- Do not change the database schema.
- You must use Go to execute the query and generate the JSON file. You will likely need to initialize a Go module and fetch the `github.com/mattn/go-sqlite3` driver.
- The output file must be written exactly to `/home/user/recommendations.json`.