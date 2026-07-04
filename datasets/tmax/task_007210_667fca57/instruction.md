You are an MLOps engineer tasked with investigating a silent data corruption issue in your training pipelines. Recently, a bug caused some integer columns to be silently converted to floats when NaNs were introduced. 

Experiment artifact metadata is stored as JSON files in `/home/user/artifacts/`. Each JSON file contains a `run_id`, a `description`, and a `schema` object detailing the column names and their inferred data types.

Your task is to identify the corrupted runs, analyze their descriptions, and find the one that most closely matches the known issue pattern.

Please complete the following steps:
1. Examine the JSON files in `/home/user/artifacts/`. Identify all runs where the data type for the column `click_count` in the `schema` is explicitly listed as `"float64"`. Runs where it is `"int64"` are healthy.
2. Extract the `run_id` of all corrupted runs and save them to `/home/user/corrupted_runs.txt`, with one `run_id` per line, sorted alphabetically.
3. You need to perform semantic search on the descriptions of these corrupted runs. Install any necessary Python packages (e.g., `sentence-transformers`, `scikit-learn`) to your environment.
4. Using the `all-MiniLM-L6-v2` model from `sentence-transformers`, compute the embeddings for the `description` fields of *only* the corrupted runs.
5. Compute the cosine similarity between those descriptions and the following reference query: `"Silent integer to float conversion due to NaN values in pipeline"`
6. Identify the `run_id` of the corrupted run whose description has the highest cosine similarity to the reference query.
7. Save exactly that single `run_id` string to `/home/user/closest_issue.txt`.

Ensure your final files match the requested names and formats perfectly.