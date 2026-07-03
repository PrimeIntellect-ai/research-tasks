You are a data engineer building an ETL pipeline to extract a social interaction graph from a raw relational database. 

You have been provided with a SQLite database at `/home/user/activity.db` containing raw application logs. The database has the following schema:
- `users` (`user_id` INTEGER PRIMARY KEY, `name` TEXT)
- `posts` (`post_id` INTEGER PRIMARY KEY, `author_id` INTEGER, `content` TEXT)
- `comments` (`comment_id` INTEGER PRIMARY KEY, `post_id` INTEGER, `commenter_id` INTEGER, `content` TEXT)

Right now, the tables do not have any indexes other than the primary keys, making complex queries extremely slow. 

Your task is to:
1. **Index Strategy Design**: Connect to the SQLite database and create appropriate indexes to optimize querying the interactions between commenters and post authors.
2. **Graph Projection & Complex Joins**: Write a single SQL query that extracts a weighted directed graph of interactions. A directed edge goes from a `commenter_id` (source) to the post's `author_id` (target). The `weight` of the edge is the total number of comments made by the source user on posts written by the target user. Do NOT include self-loops (where a user comments on their own post).
3. **Materialization**: Write and execute a Python script at `/home/user/etl_graph.py` that connects to `/home/user/activity.db`, executes your optimized query, and materializes the graph into a JSON file at `/home/user/graph_materialized.json`. 
4. **Result Processing**: Your Python script should also calculate the user with the highest total incoming edge weight (the user who received the most comments from *other* users) and write just their integer `user_id` to a text file at `/home/user/top_influencer.txt`.

The output JSON file `/home/user/graph_materialized.json` must exactly match this structure:
```json
{
  "nodes": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "edges": [
    {"source": 2, "target": 1, "weight": 5}
  ]
}
```
*Note: The `nodes` array must contain all users that exist in the `users` table, regardless of whether they have any edges.*

Ensure all files are created in `/home/user/`. Execute your Python script to generate the final output files before finishing.