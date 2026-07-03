You are acting as a database administrator. We have a Python script at `/home/user/get_2nd_degree.py` that connects to an SQLite database (`/home/user/graph.db`). This database represents a social graph with nodes (users) and directed edges (friendships).

The script is supposed to find all "2nd-degree connections" for a given user. A 2nd-degree connection is defined as a user who is a friend of a friend, but is NOT the starting user themselves, and is NOT a direct (1st-degree) friend of the starting user. 

Currently, the SQL query inside `/home/user/get_2nd_degree.py` is severely broken. It contains an implicit cross join (missing join conditions) and is returning entirely incorrect results (and far too many of them). 

Your task:
1. Analyze the schema of `/home/user/graph.db` to understand the data model and relationship mapping.
2. Fix the Python script `/home/user/get_2nd_degree.py`. Rewrite the SQL query so that it safely and efficiently retrieves the names of the 2nd-degree connections for the `user_id` passed via the parameterized query. Ensure you eliminate duplicates.
3. Once fixed, execute the script for `user_id = 1` and pipe the output to a file named `/home/user/result.txt`. The output should just be a newline-separated list of names, sorted alphabetically.

Do not change the command-line argument signature of the Python script. Just fix the query and result processing inside it, run it, and save the output.