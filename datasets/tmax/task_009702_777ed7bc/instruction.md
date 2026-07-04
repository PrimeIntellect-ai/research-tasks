You are a data engineer tasked with fixing and extending a broken ETL pipeline for product reviews.

Currently, the ETL pipeline script at `/home/user/pipeline.py` attempts to join `/home/user/data/reviews.csv` with `/home/user/data/users.csv`. However, due to missing user records, the merge silently introduces NaNs, which converts the `user_id` and `review_id` columns from integers to floats. This breaks downstream database ingestion.

Your objectives are:

1. **Fix the ETL Bug**: Modify the script to correctly handle the missing data. Any missing `is_verified` values should default to `False`. The `review_id` and `user_id` columns MUST remain integer types (you may use pandas' nullable integer type `Int64`). Save the final cleaned dataframe as a Parquet file at `/home/user/processed/cleaned.parquet`.

2. **Compute Embeddings & Retrieval**: Extend the pipeline to compute text embeddings for the `text` column using the `sentence-transformers` library (use the `all-MiniLM-L6-v2` model). Once embeddings are computed, find the top 3 `review_id`s whose text is most cosine-similar to the query: `"Excellent camera and battery life"`.
   Save the top 3 `review_id`s as a JSON list of integers in `/home/user/processed/top_3.json` (e.g., `[104, 110, 102]`).

3. **Hypothesis Testing**: We want to know if verified users write longer reviews. Perform an independent two-sample t-test (Welch's t-test, unequal variances) comparing the character length of the `text` column between verified users (`is_verified == True`) and unverified users (`is_verified == False`). 
   Save the results as a JSON object in `/home/user/processed/stats.json` with the exact key `"p_value"` containing the float p-value.

Notes:
* The data directory is `/home/user/data/`.
* You will need to install any required libraries (e.g., `pandas`, `pyarrow`, `sentence-transformers`, `scipy`).
* Create the `/home/user/processed/` directory before saving your files.