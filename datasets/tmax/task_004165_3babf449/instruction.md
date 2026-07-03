You are a data engineer working on an ETL pipeline for a social network analytics platform. 

We have an SQLite database located at `/home/user/network.db` with three tables:
1. `users` (`user_id` INTEGER, `name` TEXT, `region` TEXT)
2. `messages` (`msg_id` INTEGER, `sender_id` INTEGER, `receiver_id` INTEGER)
3. `connections` (`user1_id` INTEGER, `user2_id` INTEGER) representing an undirected friendship graph.

There is a buggy SQL script at `/home/user/aggregate.sql`. Its goal is to calculate the message volume for each user and rank them within their region using a window function. However, the query currently contains an implicit cross join, resulting in inflated and incorrect message counts for everyone.

Your task has three phases:
1. **Fix the SQL Query**: Modify `/home/user/aggregate.sql` so that it correctly computes the message count for each user (based on `sender_id`) and ranks them by `region` using `DENSE_RANK() OVER(PARTITION BY region ORDER BY message_count DESC)`. Ensure you fix the implicit cross join (use standard explicit JOIN syntax or correct WHERE clauses). Users with no messages should have a count of 0.
2. **Export the Data**: Execute the corrected query against `/home/user/network.db` and export the results to a CSV file at `/home/user/top_users.csv`. The CSV should have a header row and comma-separated values.
3. **Graph Analysis**: Identify the `#1` ranked user in the `'North'` region and the `#1` ranked user in the `'South'` region based on your CSV. Then, write a script (in Python or Bash) to compute the shortest path between these two users based on the `connections` table. The graph is undirected (an edge from A to B means an edge from B to A). 

Write the final shortest path as a comma-separated list of `user_id`s (starting with the North user and ending with the South user) to `/home/user/shortest_path.txt`.

Ensure your final output files exactly match the requested paths:
- `/home/user/aggregate.sql`
- `/home/user/top_users.csv`
- `/home/user/shortest_path.txt`