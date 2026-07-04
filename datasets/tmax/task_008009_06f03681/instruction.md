You are a data engineer building a robust ETL pipeline for a recommendation system. Standard text similarity searches can be sensitive to the exact wording. To measure the confidence of our content-based recommendations, you need to implement a pipeline that combines embedding computation, similarity search, and statistical bootstrapping.

You have been provided with two files:
1. `/home/user/word_embeddings.json`: A dictionary mapping words to their 5-dimensional float vector embeddings.
2. `/home/user/sentences.txt`: A text file containing one sentence per line. The line index (0-indexed) represents the `sentence_id`.

**Your Task:**
Write a Python script at `/home/user/etl_pipeline.py` that determines the most stable recommendation for a target sentence. 

Here is the exact algorithmic pipeline you must implement:

1. **Deterministic Baseline Embeddings:** 
   For sentences with `sentence_id` from `1` to `9`, compute their standard embedding. A sentence's embedding is the element-wise average of the vectors of its words (split by standard spaces). If a word is not in the JSON file, ignore it. 

2. **Bootstrapped Target Embeddings:**
   The target sentence is `sentence_id = 0`. To test recommendation stability, perform 100 bootstrap iterations for this target sentence.
   - For each iteration, sample $N$ words *with replacement* from the target sentence's original sequence of words, where $N$ is the number of words in the target sentence. 
   - **Important:** Use Python's built-in `random.choices()` to perform the sampling. You MUST set `random.seed(42)` exactly once at the beginning of your script.
   - Compute the bootstrapped sentence embedding as the element-wise average of the sampled words' embeddings (again, ignoring words not found in the JSON).

3. **Similarity Search & Recommendation:**
   - In each of the 100 iterations, compute the **Cosine Similarity** between the bootstrapped target embedding and the 9 deterministic baseline embeddings (IDs 1-9).
   - Find the baseline `sentence_id` that has the highest cosine similarity. If there is a tie, pick the smaller `sentence_id`.

4. **Aggregation and Output:**
   - Count how many times each baseline `sentence_id` was chosen as the top recommendation across the 100 iterations.
   - Save the results to `/home/user/recommendation_stability.csv`.
   - The CSV must have the header `neighbor_id,count`.
   - Sort the CSV by `count` in descending order. If counts are tied, sort by `neighbor_id` in ascending order.

Ensure your script runs successfully and produces the exact output file specified. Standard library modules (like `json`, `math`, `random`, `csv`) are sufficient, but you may use `numpy` or `scipy` if you prefer.