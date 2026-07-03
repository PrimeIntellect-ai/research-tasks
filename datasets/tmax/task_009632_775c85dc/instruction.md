You are acting as a data engineer. We have a C++ ETL pipeline that processes text documents, computes simplistic Bag-of-Words embeddings, and calculates the average pairwise cosine similarity across all documents. This metric is crucial for our experiment tracking.

However, we are facing two major issues:
1. **Schema Violations:** Our raw data file `/home/user/data/documents.csv` contains malformed rows. The pipeline currently crashes or produces garbage when it reads non-integer IDs.
2. **Blank Output Bug:** Even when fed perfectly clean data, the C++ program computes `0.0000` for all cosine similarities (similar to a misconfigured plotting backend rendering blank plots). This is due to a logical bug in the math/embedding computation within the C++ code.

Your tasks are:
1. **Schema Enforcement:** Modify `/home/user/src/pipeline.cpp` (or write a wrapper) to enforce the schema. A valid row MUST have exactly three columns: `id` (must be a valid integer), `text` (string), and `category` (string). Ignore/skip any invalid rows.
2. **Fix the Math Bug:** Identify and fix the bug in `/home/user/src/pipeline.cpp` that causes the cosine similarity to evaluate to zero. 
3. **Experiment Tracking:** The compiled C++ program must compute the total valid rows and the average cosine similarity of the valid dataset, and write the results to `/home/user/output/experiment_log.json` EXACTLY in this format:
```json
{
  "valid_rows": <integer>,
  "avg_similarity": <float rounded to 4 decimal places>
}
```

**Details of the embedding logic:**
The vocabulary consists strictly of 5 words: `["data", "science", "pipeline", "agent", "model"]`.
The text should be tokenized by spaces. The embedding vector is a 5-dimensional array representing the term frequency (count of the word in the document).
Cosine similarity between two vectors A and B is `dot_product(A, B) / (norm(A) * norm(B))`. If either vector has a norm of 0, the similarity is 0.
The average similarity is the sum of all unique pairwise combinations divided by the number of unique pairs. (For N documents, there are N*(N-1)/2 pairs).

**Environment Setup:**
- You have standard build tools (`g++`) installed.
- Data is located at `/home/user/data/documents.csv`.
- The broken source code is at `/home/user/src/pipeline.cpp`.
- Ensure you create the `/home/user/output/` directory if it does not exist.

Fix the code, compile it using `g++ -std=c++11 /home/user/src/pipeline.cpp -o /home/user/src/pipeline`, run it, and generate the required JSON log.