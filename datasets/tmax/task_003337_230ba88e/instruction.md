You are acting as a Data Analyst. We have a set of model predictions that need to be validated against our ground-truth dataset. Both datasets contain 3-dimensional embedding vectors. 

The datasets are located at:
1. Ground Truth: `/home/user/data/embeddings_truth.csv`
   Columns: `id`, `category`, `v1`, `v2`, `v3`
2. Model Output: `/home/user/data/embeddings_model.csv`
   Columns: `id`, `v1`, `v2`, `v3`

Your task is to write a script (in Python, R, or any suitable language) to evaluate the model's accuracy per category:
1. Merge the datasets on the `id` column.
2. For each `id`, compute the Cosine Similarity between the ground truth vector (`v1`, `v2`, `v3` from the truth file) and the model vector (`v1`, `v2`, `v3` from the model file).
3. Aggregate the results by `category`, calculating the mean cosine similarity for each category.
4. Round the mean similarities to exactly 4 decimal places (e.g., `0.8500`).
5. Save the aggregated results to `/home/user/category_metrics.csv`. The file must contain exactly two columns: `category` and `mean_similarity`, and it must be sorted alphabetically by `category`. Do not include an index column.
6. Finally, compress the resulting CSV file using `gzip` so that the final file is `/home/user/category_metrics.csv.gz`.

Complete the task and ensure the compressed file is created in the correct location with the correct schema.