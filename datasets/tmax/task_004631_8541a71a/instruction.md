You are a data scientist working on a collaborative filtering system. You have a raw dataset of user ratings located at `/home/user/ratings.csv`. The file contains three columns: `user_id`, `item_id`, and `rating`. 

Due to extraction errors, some ratings are missing (left blank), which often causes pandas to implicitly cast integer rating columns to floats with `NaN`s. 

Your task is to build a minimal item-similarity pipeline:
1. Install any necessary numerical and machine learning packages (`pandas`, `scikit-learn`, `numpy`).
2. Read `/home/user/ratings.csv`.
3. Create a user-item matrix where rows are `user_id` and columns are `item_id`. Impute any missing ratings with `0`. Ensure that your `item_id`s remain integers and do not get cast to floats (e.g., `101` not `101.0`).
4. We want to find similar items based on their rating patterns. Transpose the matrix so that items are rows and users are columns.
5. Apply dimensionality reduction to the items using `sklearn.decomposition.TruncatedSVD` with `n_components=2`. You MUST set `random_state=42` to ensure reproducibility.
6. Calculate the pairwise cosine similarity between all items in this new 2-dimensional space.
7. Identify the top 3 items most similar to item `101` (excluding `101` itself).
8. Write the integer IDs of these top 3 items, in descending order of similarity, as a comma-separated list to the file `/home/user/similar_items.txt` (e.g., `105,102,109`).

Ensure the output file contains only the comma-separated integer IDs on a single line.