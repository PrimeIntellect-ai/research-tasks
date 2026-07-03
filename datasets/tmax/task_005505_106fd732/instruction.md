You are a data engineer building a lightweight ETL pipeline and embedding retrieval system in Rust. 

Your goal is to reconstruct a simple bag-of-words embedding model, run inference on a set of documents, execute a similarity query, and track the experiment by outputting a specific JSON log.

Here is the setup:
1. You have a dictionary of pre-trained word weights located at `/home/user/model/weights.csv`. The file has no header. Each line is formatted as `word,v1,v2`, where `v1` and `v2` are floats representing a 2D embedding vector for that word.
2. You have a dataset of text documents in `/home/user/data/` (e.g., `doc1.txt`, `doc2.txt`, etc.).

Your task is to create and run a Rust project in `/home/user/etl_pipeline` that does the following:
1. Reads the `weights.csv` file into memory as a lookup table.
2. For each `.txt` file in `/home/user/data/`:
   - Tokenizes the text by splitting on whitespace (assume text is already lowercase and has no punctuation).
   - Computes the *document embedding* by calculating the element-wise **sum** of the vectors for each word in the document. Words not found in the CSV should be assigned a zero vector `(0.0, 0.0)`.
3. Processes a hardcoded search query: `"brown fox"`. Tokenize it and compute its sum embedding the exact same way as the documents.
4. Calculates the Cosine Similarity between the query vector and each document vector.
5. Identifies the document with the highest Cosine Similarity to the query.
6. Writes an experiment tracking log to `/home/user/output/experiment.json` formatted exactly like this:
```json
{
  "best_match_file": "docX.txt",
  "query_vector": [1.0, 2.0],
  "doc_vectors": {
    "doc1.txt": [2.5, 2.5],
    "doc2.txt": [-1.5, -1.5]
  }
}
```

Constraints:
- Use standard Rust (`cargo new etl_pipeline`). You may use `serde_json` and `serde` for JSON serialization.
- All numbers in the output JSON should be accurate to at least 1 decimal place.
- Do not use external ML libraries like `tch` or `tract`; reconstruct the vector sum and cosine similarity math manually.
- The pipeline must write the JSON file to exactly `/home/user/output/experiment.json`.