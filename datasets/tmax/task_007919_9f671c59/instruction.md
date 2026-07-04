You are a Machine Learning Engineer preparing a lightweight retrieval system. 

You have been provided with two files in your home directory (`/home/user/`):
1. `corpus.txt`: A small dataset of sentences, one per line.
2. `word_vectors.csv`: A CSV file containing 5-dimensional word embeddings. The format is `word,v1,v2,v3,v4,v5`.

Your task is to write a script (in any language you choose) to perform tokenization, embedding computation, retrieval, and a simple performance benchmark.

Specifically, you must:
1. **Tokenization & Embedding**: 
   - Parse `corpus.txt`. 
   - Lowercase the text and extract tokens using the regex `[a-z]+`.
   - Compute the sentence embedding as the **average** of its token embeddings.
   - If a token is not present in `word_vectors.csv`, treat its vector as `[0.0, 0.0, 0.0, 0.0, 0.0]`. 
   - If a sentence has no valid tokens, its embedding is a zero vector.
2. **Retrieval**: 
   - Using the exact same tokenization and embedding logic, compute the embedding for the following query: `"machine learning accelerates data analysis"`
   - Compute the cosine similarity between the query embedding and each sentence embedding in the corpus.
   - Identify the 0-indexed line numbers of the top 3 most similar sentences.
3. **Benchmarking**: 
   - Benchmark the inference performance: Measure the wall-clock time it takes to compute the embeddings for the *entire corpus* 1,000 times sequentially. (Do not include file I/O or tokenization in the timed portion if possible, just the vector lookup and averaging. But it's fine if you time the whole function applied 1000 times to the pre-loaded string list).

Save your final results to `/home/user/results.json` with the exact following structure:
```json
{
  "query_vector": [0.1234, 0.5678, ...], 
  "top_3_indices": [2, 5, 1],
  "benchmark_time_seconds": 0.045
}
```
*Note: Round the floats in `query_vector` to 4 decimal places. `benchmark_time_seconds` should be a standard float.*