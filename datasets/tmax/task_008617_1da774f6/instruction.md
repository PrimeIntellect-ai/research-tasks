You are a data scientist tasked with cleaning and analyzing server performance metrics using only standard Linux command-line tools (Bash, awk, sed, coreutils). 

You have a dataset located at `/home/user/raw_metrics.csv` with the following header and columns:
`server_id,cpu,mem,disk,net,state`

Perform the following data pipeline operations:

1. **Data Cleaning (Tabular Transformation):**
   Filter the dataset to keep only the header and rows where the `state` is exactly "ACTIVE" and all four numerical metrics (`cpu`, `mem`, `disk`, `net`) are greater than or equal to 0. Save this to `/home/user/cleaned.csv`.

2. **Data Augmentation (Deterministic Bootstrap):**
   Some servers are underrepresented. Create a new file `/home/user/augmented.csv` based on `cleaned.csv`. For each server row (excluding the header), duplicate the row `N` times, where `N = (cpu % 3) + 1`. Include the header exactly once at the top.

3. **Model Inference & Aggregation:**
   For every row in `augmented.csv`, compute a `health_score` using the following weighted model:
   `health_score = (cpu * 4 + mem * 3 + disk * 2 + net * 1) / 10`
   Aggregate the data to find the average `health_score` for each unique `server_id`. (Note: Because rows are identical copies, the average will equal the base score, but perform this aggregation conceptually or literally to find each server's final score).

4. **Similarity Search:**
   We want to find the server that behaves most closely to our baseline ideal health score of `50.0`. 
   Find the `server_id` whose average `health_score` has the smallest absolute difference from `50.0`. 
   If there is a tie (multiple servers have the exact same smallest absolute difference), choose the one with the highest original `cpu` value.

Write the single winning `server_id` to `/home/user/closest_server.txt`.

Ensure all output files are placed exactly as requested.