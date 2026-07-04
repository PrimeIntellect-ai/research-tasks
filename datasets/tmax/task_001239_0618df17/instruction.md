You are a data scientist tasked with cleaning a messy product dataset, generating aggregate statistics, and building a basic similarity recommendation system. 

You need to implement a data processing pipeline that is fully reproducible.

Here are your instructions:

1. You will find a dataset at `/home/user/products.csv`. It has the following columns: `id`, `name`, `category`, `price`, `description`.
2. Write a Python script at `/home/user/pipeline.py` that performs the following tasks:
   a. **Data Cleaning & Transformation**: 
      - Read the CSV. 
      - Clean the `price` column: remove the `$` character and convert it to a float. If a price is missing or cannot be converted to a float (e.g., 'invalid'), drop that entire row.
   b. **Aggregation**:
      - Calculate the average price for each `category` using the cleaned data.
      - Save this aggregated data to `/home/user/category_stats.csv`. The CSV should have two columns: `category` and `avg_price` (rounded to 2 decimal places). The rows must be sorted alphabetically by `category`.
   c. **Similarity Search & Recommendation**:
      - For the product with `id` equal to `P001`, find the top 3 most similar products in the cleaned dataset (excluding `P001` itself) based on their `description`.
      - Use **Jaccard Similarity** on the sets of words in the descriptions. To tokenize, simply convert the description to lowercase and split on standard whitespace. Do not strip punctuation. 
      - If there is a tie in Jaccard similarity, resolve it by sorting the tied product `id`s in ascending alphabetical order.
      - Save the `id`s of the top 3 recommended products to `/home/user/recommendations.txt`, with one `id` per line, ordered from most similar to least similar.

3. **Pipeline Reproducibility**:
   - Write a Bash script at `/home/user/run.sh` that runs your Python script, and then computes the SHA-256 checksums of `category_stats.csv` and `recommendations.txt`.
   - The bash script should save the checksums to `/home/user/checksums.txt` using the standard `sha256sum` format (e.g., `sha256sum category_stats.csv recommendations.txt > checksums.txt`).
   - Make sure `/home/user/run.sh` is executable.

You may use standard Python libraries. `pandas` is also available if you prefer. Do not create any files outside of `/home/user/`.