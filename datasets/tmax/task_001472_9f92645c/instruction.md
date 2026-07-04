You are an AI assistant helping a data researcher organize and validate large dataset schemas.

The researcher has set up a local environment with two microservices that manage dataset metadata:
1. A Feature Store service running on port 5001.
2. A Candidate Catalog service running on port 5002.

However, the pipeline has a known issue: the upstream pandas ingestion silently converts integer columns with missing values to floats, represented as `null` in the JSON API. 

Your task is to write a Bash script at `/home/user/dataset_recommender.sh` that takes standard input and behaves EXACTLY like our reference implementation.

For each line of standard input in the format `<query_dataset_id> <threshold>`:
1. Fetch the query dataset's feature vector by calling `http://127.0.0.1:5001/features?id=<query_dataset_id>`. The response is a JSON array of numbers or `null`s.
2. Fetch a list of candidate dataset IDs by calling `http://127.0.0.1:5002/candidates`. The response is a JSON array of strings.
3. For each candidate ID, fetch its feature vector from the Feature Store.
4. Compute the Population Covariance between the query vector and the candidate vector. 
   - Both vectors will always have the same length (N).
   - Any `null` values must be treated as `0` (this fixes the pandas artifact).
   - Population Covariance formula: `sum((x_i - mean_x) * (y_i - mean_y)) / N`.
5. Filter out candidates where the computed covariance is strictly less than the `<threshold>`.
6. Print the results to standard output in the format `<query_dataset_id> -> <candidate_id>: <covariance>` where covariance is formatted to exactly 3 decimal places.
7. For a single query, the output lines must be sorted by covariance in descending order. If there is a tie, sort by `candidate_id` in ascending alphabetical order.

Requirements:
- Your script must be written in Bash (`#!/bin/bash`).
- You may use standard Linux utilities like `jq`, `awk`, `bc`, `sort`, `curl`, etc.
- Your script must process all lines from standard input until EOF.
- Ensure your script handles multiple queries efficiently.

Make sure the file `/home/user/dataset_recommender.sh` is executable.