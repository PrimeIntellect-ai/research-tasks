You are a data analyst working on a new recommendation pipeline. We have a proprietary embedding model provided as a compiled binary, and we need to process our historical click-through rate (CTR) data to predict user interactions with new items. 

Your goal is to build a Python pipeline that uses Bayesian inference for CTR smoothing and embedding-based similarity search to predict the CTR for a set of target queries. 

Here are the specific steps and rules you must follow:

1. **Embedding Extraction**:
   You are provided with a proprietary, stripped binary at `/app/embed_oracle`. When executed with a string argument (e.g., `/app/embed_oracle "item text"`), it prints a 5-dimensional float vector separated by spaces.
   Use this binary to generate embeddings for all items listed in `/home/user/items.csv` (which has columns `item_id,item_text`).

2. **Bayesian CTR Smoothing**:
   Read the historical interactions from `/home/user/history.csv` (columns: `user_id,item_id,clicks,impressions`).
   Calculate the global prior parameters for a Beta distribution:
   - `alpha` = total sum of `clicks` across the entire history dataset.
   - `beta` = total sum of `(impressions - clicks)` across the entire history dataset.
   Compute the smoothed CTR for each user-item pair in the history using the formula:
   `smoothed_ctr = (clicks + alpha) / (impressions + alpha + beta)`

3. **Similarity-Based Prediction**:
   Read the queries from `/home/user/queries.csv` (columns: `user_id,target_item_id`).
   For each query `(u, t)`, predict the CTR for user `u` on target item `t` as follows:
   - Calculate the cosine similarity between the embedding of target item `t` and the embeddings of all items `i` that user `u` has interacted with in the history.
   - Let `weight = max(0, cosine_similarity)`.
   - `predicted_ctr = sum(weight * smoothed_ctr_i) / sum(weight)` across all historical items `i` for user `u`.
   - If `sum(weight) == 0` or the user has no history, fallback to the global mean CTR: `global_mean = alpha / (alpha + beta)`.

4. **Output**:
   Save your predictions to `/home/user/predictions.csv`. 
   The file must be a CSV with the exact header `user_id,target_item_id,predicted_ctr`.
   Round `predicted_ctr` to 6 decimal places.

A verification script will compare your predictions against a reference implementation. Your Mean Squared Error (MSE) must be below 0.0001.