You are taking over an ETL pipeline for our data engineering team. We have a legacy text embedding model compiled as a stripped Linux binary located at `/app/legacy_encoder`. It takes a single text string as a command-line argument and prints a 32-dimensional float32 vector (comma-separated) to standard output. 

Unfortunately, we lost the source code for the encoder. We do know one quirk: if the input string contains any non-alphanumeric characters (excluding standard spaces) or if it is empty, the encoder encounters a silent internal error and outputs a vector of all zeros. This has been destroying our downstream retrieval metrics.

Your task is to write a Go program (save it as `/home/user/etl.go` and compile to `/home/user/etl`) that implements the following pipeline:
1. **Tabular Transformation:** Read a CSV file located at `/app/data/events.csv`. The CSV has columns: `user_id`, `event_type`, `item_name`, `timestamp`.
2. **Aggregation:** Group the data by `user_id`. For each user, concatenate their `item_name`s in chronological order of the `timestamp`, separated by a single space.
3. **Data Sanitization:** Sanitize the concatenated string to remove any non-alphanumeric characters (keep standard ASCII spaces, but strip punctuation, symbols, and convert newlines to spaces). 
4. **Embedding Computation:** Pass the sanitized string to the `/app/legacy_encoder` binary to retrieve the embedding.
5. **Output:** Write a JSONL file to `/home/user/output.jsonl`. Each line must be a JSON object with the keys `"user_id"` (string) and `"embedding"` (array of 32 floats).

Write, compile, and run your Go pipeline. Your success will be measured by a quantitative evaluation script that calculates the Mean Squared Error (MSE) between your embeddings and our ground-truth reference embeddings.