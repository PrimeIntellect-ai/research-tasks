You are a data scientist tasked with cleaning a dataset of text documents by identifying near-duplicates, and benchmarking the similarity search inference time. 

Your environment starts with a raw dataset located at `/home/user/data.csv`. The file has two columns: `doc_id` (integer) and `text` (string).

Please perform the following steps:
1. **Analysis Environment Setup:** Install any necessary libraries (e.g., `scikit-learn`, `pandas`, `numpy`) in your Python environment.
2. **Text Processing:** Read `/home/user/data.csv`. Compute TF-IDF embeddings for the `text` column. Use the following exact parameters for the TF-IDF vectorizer to ensure consistent results:
   - Convert all text to lowercase.
   - Remove standard English stopwords (e.g., if using scikit-learn, use `stop_words='english'`).
   - Limit to the top 1000 features (`max_features=1000`).
3. **Inference Performance Benchmarking:** We need to know how fast our similarity search is for production queries. Using the computed TF-IDF matrix, measure the exact wall-clock time it takes to query the top 10 most similar documents (including itself) for the *first 100 documents* in the dataset individually (one by one) using Brute Force Cosine Distance (e.g., `sklearn.neighbors.NearestNeighbors` with `metric='cosine'`, `algorithm='brute'`). 
   - Write the total benchmarking query time in seconds (as a simple float) to `/home/user/benchmark_time.txt`.
4. **Similarity Search & Data Cleaning:** Find all unique pairs of documents that have a Cosine Similarity >= 0.85. 
   - Create a CSV file at `/home/user/duplicates.csv` with the headers `id1`, `id2`.
   - Each row should represent a duplicate pair of `doc_id`s.
   - For each pair, ensure `id1` < `id2`.
   - Sort the final CSV by `id1` ascending, and then by `id2` ascending.

Complete the tasks using standard Python tools and leave the resulting files (`/home/user/benchmark_time.txt` and `/home/user/duplicates.csv`) in place for verification.