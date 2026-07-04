You are an AI assistant helping a data researcher organize and analyze a dataset of vector embeddings representing research papers. The researcher wants to test feature redundancy, find similar papers, and benchmark a similarity search implementation. 

You need to write and execute a Go program that performs the following tasks:

1. **Read the Datasets**:
   - `/home/user/vectors.csv`: Contains the main dataset. The first column is `ID` (string), followed by 10 columns of floating-point numbers representing features `F1` to `F10`.
   - `/home/user/queries.csv`: Contains query vectors in the same format.

2. **Correlation Analysis**:
   - Calculate the Pearson correlation coefficient between feature `F1` and feature `F2` across all records in `vectors.csv`. 

3. **Similarity Search and Recommendation**:
   - For the query vector with ID `Query_1` in `queries.csv`, compute the Cosine Similarity between it and every vector in `vectors.csv`.
   - Identify the top 3 most similar vectors (highest cosine similarity) from `vectors.csv`. Return their IDs.

4. **Inference Performance Benchmarking**:
   - Benchmark the similarity search you just implemented. 
   - Time how long it takes to find the top 3 matches for `Query_1` against the entire `vectors.csv` dataset. Run this search operation in a loop 1,000 times.
   - Calculate the average execution time per search in milliseconds (ms).

5. **Reporting**:
   - Save the results to a JSON file at `/home/user/results.json` strictly matching this structure:
     ```json
     {
       "correlation_F1_F2": 0.000, // Round to 3 decimal places
       "query_1_top_3": ["ID_A", "ID_B", "ID_C"], // List of 3 string IDs in descending order of similarity
       "benchmark_avg_ms": 0.000 // Float, average time per search in milliseconds
     }
     ```

Constraints & Guidelines:
- Use **Go** (`/usr/local/go/bin/go` or standard `go` command) to write your solution. Standard library packages (`math`, `encoding/csv`, `encoding/json`, `sort`, `time`, etc.) are fully sufficient.
- Do not use external Go modules (no `go get`).
- You may use any terminal commands to test, compile, and run your code. 
- Ensure `/home/user/results.json` is created successfully with the correct data.