You are acting as a Data Analyst. You have been given a dataset of product reviews located at `/home/user/reviews.csv`. The file has three columns: `product_id`, `review_text`, and `rating`. 

Unfortunately, the data extraction pipeline was flawed, and some `rating` values are missing (empty strings). If you load this carelessly into tools like Pandas, the missing values will cause the `product_id` and `rating` columns to be silently cast to floats, which breaks our downstream strict-integer ID matching systems.

Your objective is to write a robust data processing pipeline (you may use Python, bash, or a combination) that performs the following tasks:

1. **Data Cleaning & Aggregation:**
   - Drop any rows where the `rating` is missing.
   - Ensure `product_id` is treated as a strict integer (e.g., `101`, not `101.0`).
   - For each unique `product_id`, compute its average rating.
   - For each unique `product_id`, aggregate all its `review_text` into a single string. Tokenize this aggregated text by converting to lowercase, removing all punctuation (except spaces), and splitting by whitespace to create a set of unique words (keywords) for that product.

2. **Similarity Search (Recommendation):**
   - We want to recommend products similar to Product ID `101`.
   - Calculate the Jaccard similarity between the keyword set of `101` and the keyword sets of all other products.
   - Find the top 3 most similar products (excluding `101` itself). If there is a tie, resolve it by selecting the smaller `product_id`.
   - Write the integer `product_id`s of these top 3 products, comma-separated on a single line, to `/home/user/recommendations.txt`.

3. **Hypothesis Testing:**
   - We want to know if the presence of the word "excellent" in a product's reviews is associated with higher ratings.
   - Divide all products (after cleaning) into two groups: those whose aggregated keyword set contains the exact token "excellent", and those that do not.
   - Perform an independent two-sample Welch's t-test (unequal variances) comparing the average ratings of the two groups (Group 1: has "excellent", Group 2: does not have "excellent").
   - Write the resulting p-value, rounded to exactly 4 decimal places, to `/home/user/ttest.txt`.

Ensure your scripts handle the data types correctly and that your final output files exactly match the requested names, paths, and formats.