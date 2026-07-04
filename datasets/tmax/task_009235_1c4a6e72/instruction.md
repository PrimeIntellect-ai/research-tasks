You are a data analyst setting up an experiment tracking script for a rudimentary product recommendation pipeline. 

We have a dataset of products at `/home/user/data/products.csv` with the following columns: `id`, `product_name`, and `tags`. The `tags` column contains space-separated keywords.

Your task is to write a Go program located at `/home/user/recommender.go` that acts as a reproducible similarity search step in our pipeline.

The program must accept two command-line flags:
- `-target`: an integer representing the `id` of the target product.
- `-run`: a string representing the experiment run ID.

The program should perform the following:
1. **Schema Enforcement:** Read `/home/user/data/products.csv`. Discard any rows that do not strictly adhere to this schema:
   - `id` must be a valid integer.
   - `product_name` must be a non-empty string.
   - `tags` must be a non-empty string.
2. **Similarity Search:** For the valid product matching the `-target` ID, compute the Jaccard similarity of its tags against the tags of all *other* valid products. 
   - Treat the space-separated tags as a set of strings. 
   - Jaccard similarity = (Size of Intersection) / (Size of Union).
   - Find the product with the highest Jaccard similarity. If there is a tie, break the tie by choosing the product with the lowest `id`.
3. **Experiment Tracking:** Write the result to a JSON file at `/home/user/results/run_<run_id>.json` ensuring the pipeline outputs are tracked per run. The JSON must exactly match this structure:
```json
{
  "run_id": "<run_id_string>",
  "target_id": <target_id_int>,
  "recommended_id": <recommended_id_int>,
  "similarity_score": <float64_score>
}
```

Once you have written the script, execute it with the following arguments:
`-target 3 -run exp_beta_01`

Ensure the `/home/user/results/` directory exists before writing to it.