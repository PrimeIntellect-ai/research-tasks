You are an MLOps engineer tasked with fixing an evaluation pipeline and improving the retrieval quality of a similarity search system.

We have a custom, in-house vector evaluation package located at `/app/custom_vec_eval-1.0.0`. It currently has two major issues:
1. The distance calculation in `custom_vec_eval.metrics` is mathematically incorrect, causing similarity search evaluations to return completely wrong nearest neighbors.
2. The plotting module in `custom_vec_eval.plot` produces blank or invalid plots due to a matplotlib backend misconfiguration. 

Additionally, our incoming query vectors have experienced a feature shift (a linear transformation) compared to our database embeddings. You need to learn this transformation and correct the queries.

Your tasks:
1. **Fix the Package**: Identify and fix the mathematical bug in `/app/custom_vec_eval-1.0.0/custom_vec_eval/metrics.py` (it's supposed to calculate squared Euclidean distance to find the closest embeddings, but the formula has a sign error). Also, fix the backend in `/app/custom_vec_eval-1.0.0/custom_vec_eval/plot.py` so that it successfully saves valid PNG files. Install your fixed package using `pip install -e /app/custom_vec_eval-1.0.0`.
2. **Align the Queries**: 
   - Load the database embeddings from `/home/user/embeddings.npy` (shape: 1000x50).
   - Load the shifted queries from `/home/user/queries_raw.npy` (shape: 100x50).
   - Load the ground truth indices from `/home/user/ground_truth.npy` (shape: 100, representing the true matching embedding index for each query).
   - Use the first 20 queries (indices 0 to 19) and their corresponding target embeddings (fetched using the ground truth indices) as a training set. Train a multiple linear regression model (finding a weight matrix and bias) to map the raw queries to their true embedding space.
   - Apply this learned transformation to **all 100 queries**. Save these corrected queries to `/home/user/queries_fixed.npy`.
3. **Generate Artifacts**: Use your fixed `custom_vec_eval` package to compute the Recall@10 for your corrected queries across the entire dataset. Use the `plot_recall` function to generate and save a bar chart to `/home/user/recall_plot.png`.

An automated verifier will evaluate the Recall@10 of your `/home/user/queries_fixed.npy` on the test set (the last 80 queries). You must achieve a Recall@10 of at least 0.85 on the test set.