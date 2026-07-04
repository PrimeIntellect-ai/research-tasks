I need your help fixing and optimizing our graph processing pipeline for fraud detection.

We have a system with two services currently running:
1. A Transaction API running locally on `http://localhost:8080`. It serves transaction data in CSV format via the `/transactions` endpoint. It supports pagination via `?page=<int>`.
2. A Redis server running on `localhost:6379`.

Your goal is to write a Python script at `/home/user/workspace/pipeline.py` that does the following:
1. Fetches all pages of transactions from the Transaction API until it returns an empty response. 
   *Note: Due to a known issue with the API's pagination cursor, some pages return overlapping/stale rows. You must deduplicate transactions using the `tx_id` column.*
2. Builds a directed graph of these transactions. The columns are `tx_id`, `sender_id`, `receiver_id`, `amount`, and `timestamp`. The graph edges should go from `sender_id` to `receiver_id`, with the sum of `amount` between them as the edge weight.
3. Computes the Personalized PageRank (PPR) for all nodes in the graph. The "personalization" dictionary should assign a value of `1.0` to the known fraudulent accounts: `U-991`, `U-042`, and `U-777` (and `0.0` or omitted for all others). Use a damping factor (alpha) of `0.85` and the edge weights for the computation.
4. Retrieves the top 100 most suspicious accounts (highest PPR score) excluding the initial known fraudulent accounts.
5. Pushes these top 100 accounts into the Redis server into a Sorted Set named `fraud_scores`. The score in the sorted set should be the PPR score, and the member should be the account ID.

Requirements:
- Code must be written in Python 3.
- You can use the `networkx`, `requests`, `pandas`, and `redis` libraries.
- **Performance:** Your pipeline must be highly efficient. The metric evaluated is the F1-score/overlap of your top 100 nodes compared to the exact mathematical top 100, and it must execute within a strict time limit.
- Run your script and ensure the Redis sorted set `fraud_scores` is fully populated. Finally, create an empty file `/home/user/workspace/done` when you are finished.