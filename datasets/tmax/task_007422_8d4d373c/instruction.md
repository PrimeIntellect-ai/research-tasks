You are an MLOps engineer tasked with evaluating and tracking the results of two different embedding models (Experiment A and Experiment B) for a similarity search task. 

In `/home/user/data/`, you will find three numpy files:
1. `experiment_A_items.npy`: Item embeddings from Model A (shape: N x D).
2. `experiment_B_items.npy`: Item embeddings from Model B (shape: N x D).
3. `queries.npy`: A set of query embeddings (shape: M x D).

Your goal is to write and execute a Python script `/home/user/evaluate_models.py` that performs the following steps:

1. **Model Output Validation**: 
   - Load the queries. Some query vectors might be corrupted and contain `NaN` values. Identify and discard any queries that contain one or more `NaN` values. Keep track of the *original* query indices (0 to M-1) for the valid queries.
   - Load the item embeddings for both experiments.
   - Ensure all valid query embeddings and all item embeddings are L2-normalized. If they are not L2-normalized (norm != 1.0), normalize them.

2. **Similarity Search**:
   - For each valid query, compute the cosine similarity against all items in Experiment A and all items in Experiment B.
   - For each valid query and for each experiment, find the indices of the **Top-3** most similar items (highest cosine similarity).

3. **Experiment Tracking Log**:
   - Save the results to `/home/user/experiment_results.json`.
   - The JSON file must perfectly match the following structure:
     ```json
     {
       "valid_queries_count": <integer>,
       "experiment_A": {
         "<original_query_index>": [<item_idx_1>, <item_idx_2>, <item_idx_3>],
         ...
       },
       "experiment_B": {
         "<original_query_index>": [<item_idx_1>, <item_idx_2>, <item_idx_3>],
         ...
       }
     }
     ```
   - Note: The keys in `experiment_A` and `experiment_B` should be strings of the original query indices (e.g., `"0"`, `"1"`, `"2"`... skipping any that had NaNs). The lists should contain exactly 3 integers representing the indices of the top 3 items in descending order of similarity.

Ensure your script runs successfully and generates the exact JSON file requested.