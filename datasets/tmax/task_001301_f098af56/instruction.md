You are a data engineer building a core ETL pipeline for a recommendation system. You need to process user and item embeddings to find the best match for each user.

Your tasks are:
1. Create a Python virtual environment at `/home/user/venv`.
2. Install necessary data science packages (e.g., `pandas`, `numpy`) into this virtual environment.
3. Write and execute a script (in Python) that reads two files:
   - `/home/user/users.csv` (Columns: `user_id`, `f1`, `f2`, `f3`, `f4`)
   - `/home/user/items.csv` (Columns: `item_id`, `f1`, `f2`, `f3`, `f4`)
4. For each `user_id`, calculate the dot product of their feature vector (`f1` to `f4`) against all item feature vectors.
5. Identify the `item_id` that yields the highest dot product score for each user.
6. Save the results to `/home/user/top_matches.csv`. The file must have exactly the columns `user_id,item_id,score` in a comma-separated format. Round the `score` to exactly 4 decimal places. Sort the output by `user_id` in ascending order.

Ensure your code is efficient and strictly follows the output formatting.