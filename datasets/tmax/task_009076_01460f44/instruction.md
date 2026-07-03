You are a data analyst tasked with migrating relational social network data from flat CSV files into a document-oriented structure suitable for a NoSQL database. You need to combine relational mapping, graph processing, and aggregation pipelines into a single Python script.

You have been provided with three CSV files in the `/home/user/` directory:
1. `users.csv` - Schema: `id,name`
2. `follows.csv` - Schema: `follower_id,followed_id` (Directed edges: follower_id follows followed_id)
3. `posts.csv` - Schema: `post_id,author_id,views`

Your objective is to write and execute a Python script that processes these CSVs and outputs a single JSON Lines file (`/home/user/user_profiles.jsonl`). 

Each line in the JSONL file must represent a user document with the following exact keys:
- `user_id`: Integer, the user's ID.
- `name`: String, the user's name.
- `total_post_views`: Integer, the sum of `views` for all posts authored by the user. If they have no posts, this should be 0.
- `second_degree_follows`: A sorted list of Integers representing the IDs of "second-degree follows".

**Rules for `second_degree_follows`:**
A user 'A' has a second-degree follow to user 'C' if and only if:
1. 'A' follows some user 'B'.
2. 'B' follows 'C'.
3. 'A' does NOT directly follow 'C'.
4. 'C' is NOT 'A' (a user cannot be their own second-degree follow).

**Output Requirements:**
- The resulting file must be saved to `/home/user/user_profiles.jsonl`.
- The file must contain exactly one JSON object per line.
- The lines must be sorted by `user_id` in ascending order.
- Do not use external libraries other than standard Python libraries (e.g., `csv`, `json`, `collections`).