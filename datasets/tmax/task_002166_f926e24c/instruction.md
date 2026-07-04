You are a Machine Learning Engineer preparing training data and building a simple recommendation pipeline. 

You have been given three datasets in `/home/user/`:
1. `users.csv` (Contains all registered users)
2. `purchases.csv` (Contains user purchase history)
3. `products.csv` (Contains product metadata)

Your task is to write a Python script that does the following:
1. Merges the datasets to find all purchases made by each user. **Warning:** If you perform a `LEFT JOIN` from users to purchases, users with no purchases will introduce `NaN` values, which pandas will use to silently convert the `product_id` column from integers to floats. Your pipeline must explicitly prevent or fix this. Any user with no purchases should be completely dropped from the analysis, and `product_id` must be processed as strict integers, not floats.
2. Computes the Jaccard similarity between `user_id=1` and all other valid users based on the sets of `product_id`s they have purchased.
3. Identifies the single most similar user to `user_id=1` (highest Jaccard similarity). If there is a tie, pick the user with the smallest `user_id`.
4. Finds the products that this most similar user has purchased, but `user_id=1` has NOT purchased.
5. Selects the smallest `product_id` from this set of candidate products as the final recommendation.

Write the final recommended integer `product_id` to a file located at `/home/user/recommendation.txt`.