You are a data analyst working with exported social network data. You have been given two CSV files located in `/home/user/data/`:
- `users.csv` (columns: `id`, `username`)
- `connections.csv` (columns: `user1_id`, `user2_id`)

The `connections.csv` file represents undirected friendships. This means if `user1_id` is connected to `user2_id`, both users should be credited with 1 friend. 

Your task:
1. Parse the CSV files to calculate the total number of friends (the degree centrality) for each user.
2. Sort the users by their friend count in descending order.
3. If there is a tie in friend count, sort the tied users by their `username` alphabetically (ascending).
4. Take the top 3 users (pagination/filtering) based on this sorting.
5. Export the result to `/home/user/output.json` in the exact JSON format shown below:

```json
[
  {
    "username": "aaron",
    "friend_count": 4
  },
  ...
]
```

Ensure the output is a valid JSON array of objects containing exactly 3 items. Do not include headers from the CSV in your calculations. You may write a Bash, Python, or Awk script to accomplish this.