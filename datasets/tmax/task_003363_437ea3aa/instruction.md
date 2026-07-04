You are a data analyst investigating a potential bug in a new similarity recommendation model. The model outputs nearest neighbors, but you suspect its distance calculations are numerically inaccurate. You need to validate its output by calculating a baseline Euclidean distance using standard command-line tools.

You are provided with a file: `/home/user/vectors.csv`
This file contains 1,000 rows of item embeddings. It has no header. 
The columns are: `item_id, v1, v2, v3, v4, v5` (comma-separated).

Your task:
1. Extract the vector for the target item: `item_id` = "target_842".
2. Calculate the Euclidean distance between "target_842" and all other items in the dataset (do not calculate the distance to itself).
3. Find the 5 items with the smallest Euclidean distance to "target_842".
4. Write the `item_id`s of these top 5 closest items to `/home/user/top5_baseline.txt`, with one `item_id` per line, sorted from closest (smallest distance) to 5th closest.

You must accomplish this using Bash and standard Linux text processing tools (like `awk`, `sort`, `head`, etc.).