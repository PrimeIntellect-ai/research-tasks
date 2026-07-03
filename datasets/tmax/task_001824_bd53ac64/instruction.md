You are a data engineer tasked with building an end-to-end ETL pipeline and a similarity recommendation service for a new content platform.

Your environment has a raw dataset of articles located at `/home/user/raw_data.jsonl`. Each line is a JSON object with the keys `"id"` (string) and `"text"` (string).

Your task has three phases:
1. **Extract & Transform (Tokenization and TF-IDF):**
   - Read the dataset.
   - Tokenize the `"text"` field for each document: convert to lowercase, remove all characters except alphanumeric characters and spaces, and split by spaces. Ignore empty string tokens.
   - Compute the TF-IDF vector for each document. 
     - TF (Term Frequency) = the raw count of the term in the document.
     - IDF (Inverse Document Frequency) = `ln(N / df)`, where `N` is the total number of documents, `df` is the number of documents containing the term, and `ln` is the natural logarithm.
   - Note: The vocabulary should be built from all tokens across all documents.

2. **Load (Large-scale Data Storage):**
   - Store the extracted data (and/or your computed vectors) in an SQLite database located at `/home/user/etl_store.db`. You may design the schema however you like, but the database must contain the necessary information to serve recommendations without re-parsing the JSONL file.

3. **Serve (Similarity Search API):**
   - Write and start a background web server listening on `127.0.0.1:8080`.
   - The server must expose a GET endpoint `/similar?id=<doc_id>`.
   - When called, it should compute the cosine similarity between the TF-IDF vector of the requested document and all other documents.
   - It must return a JSON response with the top 3 most similar document IDs (excluding the queried document itself), ordered from highest similarity to lowest. Tie-breaker should be the document ID in alphabetical order.
   - Response format: `{"similar_ids": ["doc_X", "doc_Y", "doc_Z"]}`

After starting the server in the background, use `curl` or any other tool to query the endpoint for `id=doc1` and save the raw JSON response to `/home/user/doc1_recommendations.json`. Leave the server running.