You are a Data Analyst stepping into a project where the previous engineer left abruptly. You need to build a robust data processing pipeline in Bash.

We have a dataset of ad traffic at `/app/data/traffic.csv` with the following columns:
`id,clicks,impressions,emb_x,emb_y,emb_z`

Your goal is to calculate a Bayesian adjusted click-through rate (Posterior CTR) for each ad, filter them based on their embedding similarity to a target profile, and output the top candidates.

Here are the specific requirements:
1. **Extract Parameters**: Our lead statistician left a scanned note at `/app/prior_specs.png`. You must use OCR (e.g., `tesseract`) to read this image and extract three numbers: the Beta prior's `Alpha` value, `Beta` value, and the `Similarity_Threshold`.
2. **Handle Missing Data**: The CSV contains missing values (empty fields). Standard shell tools (like awk) often silently convert empty strings to zeros, which corrupts statistical calculations. You must handle missing data explicitly:
   - Impute missing `impressions` to 100.
   - Impute missing `clicks` to 0.
3. **Bayesian Inference**: Compute the Posterior CTR for each row using the formula:
   `Posterior_CTR = (clicks + Alpha) / (impressions + Alpha + Beta)`
4. **Embedding Retrieval**: Compute the Cosine Similarity between each row's embedding vector `[emb_x, emb_y, emb_z]` and our target profile vector `T = [1.0, 0.0, 0.0]`.
5. **Filtering and Sorting**: 
   - Filter out any rows where the Cosine Similarity is *strictly less* than the `Similarity_Threshold` extracted from the image.
   - Sort the remaining rows by `Posterior_CTR` in descending order. Break ties by `id` in ascending order.
6. **Output**: Write a primary Bash script at `/home/user/run_analysis.sh` that performs this entire pipeline when executed. The script should output a final CSV file at `/home/user/top_candidates.csv` containing the top 50 rows, with exactly these columns (include a header):
   `id,posterior_ctr,similarity`

Make sure your math is numerically accurate (use at least 5 decimal places for intermediate calculations).