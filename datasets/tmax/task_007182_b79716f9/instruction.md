You are a data analyst working with a dataset of user interactions in a forum. 

We have a CSV file located at `/home/user/data/comments.csv` with two columns: `user_id` and `thread_id`.
We want to project this bipartite data into a user-user network graph. Specifically, an undirected edge should exist between two users if they have both commented on the same `thread_id`.

I started writing a C program to read this CSV, map the sparse `user_id`s to dense array indices using an indexing strategy, and compute some basic graph analytics. However, my code (`/home/user/project_graph.c`) has a critical bug: it seems to be creating an implicit cross-join, connecting almost every user to every other user regardless of the `thread_id`! It is also missing a proper index strategy (like a binary search or hash map) to map the raw `user_id` integers to dense node IDs `0...N-1`.

Your task:
1. Fix the logic in `/home/user/project_graph.c` so that it correctly materializes the graph. Two distinct users should only have an edge if they share at least one `thread_id`.
2. Implement a proper indexing strategy in the C code to map the `user_id`s to dense array indices so the graph can be stored efficiently in an adjacency matrix or edge list.
3. Compute the total number of unique, undirected edges in the projected graph (do not count self-loops, and do not double-count (A,B) and (B,A)).
4. Compute the `user_id` that has the highest degree (most connections to other users). If there is a tie, pick the smallest `user_id`.
5. Compile and run your fixed C program.
6. Write the final results to a JSON file at `/home/user/metrics.json` with the following exact structure:
```json
{
  "total_unique_edges": 123,
  "max_degree_user_id": 4567
}
```

Ensure your C program is self-contained, compiles with `gcc -O2 /home/user/project_graph.c -o /home/user/project_graph`, and executes efficiently.