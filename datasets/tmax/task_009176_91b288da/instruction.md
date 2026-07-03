You are a database administrator dealing with a stale materialized view and graph processing in a social network database. 

We have an SQLite database located at `/home/user/network.db`. 
By reverse engineering the schema, you will see it contains a `users` table and a `follows` table, representing the canonical state of user relationships. There is also an `active_follows` table which is used as a materialized cache for fast querying, but it has become corrupted and contains "stale" rows (relationships that no longer exist in the canonical `follows` table, or references to `user_id`s that have been deleted).

Your tasks are as follows:

1. **Clean the Data**: Identify and delete all stale rows from the `active_follows` table. A row in `active_follows` is valid *only if* the `(follower_id, followee_id)` pair exists in the `follows` table AND both user IDs exist in the `users` table.

2. **Graph Materialization & Analytics**: Using Python (you can use the `networkx` library, install it if necessary), materialize the cleaned `active_follows` table into a Directed Graph.
   
3. **Compute Centrality**: Calculate the PageRank of all nodes in this directed graph. Use the standard NetworkX PageRank implementation with default parameters (`alpha=0.85`, `max_iter=100`, no weights).

4. **Output Generation**: Identify the top 5 users with the highest PageRank scores. Write the results to `/home/user/top_users.csv`. The CSV must have exactly this header: `user_id,username,pagerank`. Sort the output in descending order of PageRank. Round the `pagerank` values to exactly 4 decimal places.

Ensure the final CSV file is correctly formatted and placed at `/home/user/top_users.csv`. You may create any intermediate Python scripts or SQL queries you need.