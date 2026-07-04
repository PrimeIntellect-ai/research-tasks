You are a data engineer building an ETL pipeline to analyze user influence in a social network. 

You have been provided with an SQLite database at `/home/user/social_data.db` containing four tables:
- `users`: `user_id` (INTEGER), `name` (TEXT)
- `friendships`: `user_id1` (INTEGER), `user_id2` (INTEGER) - represents an undirected friendship.
- `posts`: `post_id` (INTEGER), `user_id` (INTEGER), `content` (TEXT)
- `engagements`: `post_id` (INTEGER), `likes` (INTEGER), `shares` (INTEGER)

Your task is to write a Python script at `/home/user/etl_pipeline.py` that chains together SQL queries and Python graph processing to extract and materialize influencer metrics. The pipeline must do the following:

1. **Graph Projection**: Extract the friendship data and build an undirected graph in Python. Calculate the "degree" of each user (the total number of unique friends they have). Note that the `friendships` table might only list a pair once (e.g., 1 and 2), but it means both user 1 and user 2 have a degree of at least 1.
2. **Complex Joins**: Calculate the total engagements (sum of `likes` + `shares`) for all posts made by each user. 
3. **Pipeline Chaining & Materialization**: Combine the user details, their computed graph degree, and their total engagements. 
4. **Filtering**: Only include users who have a degree of **2 or higher**.
5. **Output**: Write the final materialized data to a JSON file at `/home/user/influencer_metrics.json`.

The JSON file must be a list of dictionaries, formatted exactly like this:
```json
[
  {
    "user_id": 1,
    "name": "Alice",
    "degree": 3,
    "total_engagements": 150
  },
  ...
]
```
The list must be sorted by `total_engagements` in strictly descending order. If there is a tie in engagements, sort by `user_id` in ascending order. Users with no posts or engagements should have a `total_engagements` of 0.

Run your script to generate the `/home/user/influencer_metrics.json` file.