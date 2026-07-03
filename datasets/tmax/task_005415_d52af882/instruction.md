You are a data analyst tasked with processing a messy dataset of user-item ratings. The data engineering team noticed that an upstream pipeline silently introduced missing values ("NaN", "NA", "null", or empty strings) into the `rating` column instead of proper integers. 

Your task is to write a Go program `/home/user/process.go` that processes this large CSV file, imputes the missing ratings using a simple Bayesian approach, and finds the most similar items to a target item using Cosine Similarity.

Here are the requirements:
1. **Dataset**: `/home/user/ratings.csv` contains headers `user_id,item_id,rating`.
2. **Valid vs. Missing Ratings**: Any rating that can be parsed as a valid numeric value is considered valid. Values like "NaN", "NA", "null", or "" are missing.
3. **Bayesian Imputation**:
   - First, calculate the global mean (`m`) of all *valid* ratings in the dataset.
   - For each `item_id`, compute its Bayesian average rating:
     `bayesian_avg = (5.0 * m + sum_of_valid_ratings_for_item) / (5.0 + count_of_valid_ratings_for_item)`
   - If a user has a row for an item but the rating is missing, replace it with that item's `bayesian_avg`.
4. **Vector Representation**: 
   - Represent each item as a vector where each dimension corresponds to a `user_id` (lexicographically ordered).
   - If a user has a row for an item, their value in the vector is the valid rating or the imputed `bayesian_avg`.
   - If a user does NOT have a row for an item in the dataset, their value in the vector is `0.0`.
5. **Similarity Search**:
   - Compute the Cosine Similarity between the item `"I42"` and all other items based on their user vectors.
   - Cosine Similarity = `dot(A, B) / (norm(A) * norm(B))`. If either norm is 0, similarity is 0.
6. **Output**:
   - Write the top 3 most similar items to `"I42"` (excluding `"I42"` itself) to `/home/user/top_items.csv`.
   - The CSV should have no header, and each row must be `item_id,similarity`.
   - The similarity scores must be rounded to exactly 4 decimal places (e.g., `0.1234`).
   - Break ties by `item_id` in ascending lexicographical order.

You may use standard Go library packages only. Build and run your Go script to produce the output file.