You are a data engineer tasked with building an ETL pipeline to compute product recommendations based on text descriptions.

We have a vendored Approximate Nearest Neighbors (ANN) package located at `/app/tiny_ann` that we need to use for similarity search in our pipeline. However, the package currently fails to install due to a configuration bug introduced in the last commit.

Your objectives:
1. Fix the installation issue in the vendored `/app/tiny_ann` package and install it in your environment.
2. Write an ETL script `/home/user/etl_pipeline.py` that performs the following steps:
   - Reads a dataset of product descriptions from `/home/user/data/items.csv` (columns: `item_id`, `description`).
   - Uses `scikit-learn` to compute TF-IDF vectors for the descriptions (use english stop words, max_features=500).
   - Reduces the dimensionality of the vectors to 50 dimensions using `TruncatedSVD` (random_state=42).
   - Indexes these 50-dimensional vectors using the `tiny_ann.TinyIndex` class from the fixed package.
   - Reads a set of query items from `/home/user/data/queries.csv` (columns: `query_id`, `description`), applies the same TF-IDF and SVD transformations.
   - Queries the `TinyIndex` to find the top 5 most similar `item_id`s for each query.
3. Save the results to `/home/user/recommendations.csv`. The output CSV must have two columns: `query_id` and `recommended_item_ids` (a space-separated string of the 5 recommended item IDs).

The automated evaluation will compare your recommended items against exact brute-force cosine similarity recommendations. You must achieve a Recall@5 metric of at least 0.85 to pass.