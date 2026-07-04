You are an AI assistant helping a researcher organize and analyze a text dataset.

The researcher wants to build a reproducible pipeline in Rust that computes custom "embeddings" for text data, stores them efficiently, and allows for similarity retrieval. 

Here is the specification for the task:

1. **The Dataset**: There is a dataset located at `/home/user/dataset.csv` with two columns: `id` (integer) and `text` (string).
2. **The Embedding Function**: To keep things fast and deterministic without external models, we define a text's embedding as a 5-dimensional vector counting the occurrences of vowels (case-insensitive) in the text: `[count(a), count(e), count(i), count(o), count(u)]`.
3. **Data Storage**: Create a Rust project named `vowel_embedder` in `/home/user/vowel_embedder`. Write a program that reads `dataset.csv`, computes the 5-dimensional embedding for each row, and stores the results in a SQLite database at `/home/user/embeddings.db`. The database should have a table named `embeddings` with the schema: `(id INTEGER PRIMARY KEY, a INTEGER, e INTEGER, i INTEGER, o INTEGER, u INTEGER)`.
4. **Retrieval**: Your Rust program should accept a command-line argument `--query <id>`. When provided, the program must calculate the Squared Euclidean Distance between the embedding of the specified `<id>` and all *other* embeddings in the database. 
5. **Output**: The program should find the `id` of the text with the smallest squared Euclidean distance to the query ID, and print *only* that closest `id` to standard output. (If there is a tie, pick the one with the smallest `id`).
6. **Pipeline Integration**: Write a bash script at `/home/user/run_pipeline.sh` that:
   - Compiles the Rust project in release mode.
   - Runs the ingestion to create/populate `/home/user/embeddings.db`.
   - Runs the query tool for `--query 42` and redirects the output (the closest ID) to `/home/user/closest.txt`.

Ensure your `run_pipeline.sh` is executable and run it to produce the final `closest.txt` file. You may use standard crates like `csv`, `rusqlite`, and `clap` in your Rust project.