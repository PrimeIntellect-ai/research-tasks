You are an AI assistant helping a mathematical researcher organize a dataset of document embeddings. 

The researcher has a dataset of 5-dimensional embeddings representing different research papers, stored at `/home/user/embeddings.csv`. 
The file has a header row: `id,v1,v2,v3,v4,v5`.

Your task is to build a robust Rust command-line tool that performs embedding computation and retrieval to find the most similar papers to a new, unindexed draft paper.

Follow these instructions exactly:
1. Create a new Rust project in `/home/user/retrieval_tool` using Cargo.
2. The draft paper has the following embedding vector: `[0.12, 0.88, 0.34, 0.71, 0.55]`.
3. Write a Rust program that calculates the Cosine Similarity between this draft vector and every vector in `/home/user/embeddings.csv`. Use 64-bit floats (`f64`) for all calculations to ensure numerical accuracy.
4. The formula for cosine similarity between vectors A and B is: `(A · B) / (||A|| * ||B||)`.
5. Identify the top 3 most similar vectors (highest cosine similarity). If there is a tie, break it by selecting the lower `id`.
6. Output the results as a JSON array of objects to `/home/user/top_matches.json`. Each object must have the integer `id` and the `similarity` score rounded to exactly 6 decimal places.

Example of expected output format in `/home/user/top_matches.json`:
```json
[
  {
    "id": 4,
    "similarity": 1.000000
  },
  {
    "id": 0,
    "similarity": 0.998432
  },
  {
    "id": 2,
    "similarity": 0.873211
  }
]
```

To complete this task, you will need to set up the Rust environment, write the code, manage dependencies (e.g., `csv`, `serde_json` if needed), compile, and run the pipeline. Ensure your results are fully reproducible.