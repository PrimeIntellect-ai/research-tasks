You are a data engineer at a fast-growing e-commerce startup. Your task is to build a lightweight ETL pipeline and an item-to-item recommendation engine based on product descriptions. 

You have been provided with a raw data file at `/home/user/raw_products.jsonl`. This file contains newline-delimited JSON records.

Your objective is to process this data, perform similarity search, and generate recommendations for a specific set of target products. You may use any programming language and libraries you prefer (e.g., Python with `scikit-learn`), but you must install any non-standard dependencies yourself in your environment.

**Step 1: ETL & Preprocessing**
1. Read the data from `/home/user/raw_products.jsonl`.
2. Filter out any products where the `description` field is missing, `null`, or consists only of whitespace.
3. Clean the `description` for the remaining products:
   - Convert all text to lowercase.
   - Remove all punctuation (replace with spaces).
   - Collapse multiple spaces into a single space.

**Step 2: Similarity Modeling**
1. Convert the cleaned descriptions into TF-IDF vectors.
2. Compute the pairwise Cosine Similarity between all valid products based on their TF-IDF vectors.

**Step 3: Recommendation Generation**
Generate the top 3 recommended (most similar) products for the following target Product IDs:
- `"P001"`
- `"P005"`
- `"P009"`

Constraints for recommendations:
- Do not include the target product itself in its recommendations.
- For each target product, identify the 3 products with the highest cosine similarity.
- To ensure a standardized output format, **sort the 3 recommended Product IDs alphabetically** for each target product.

**Step 4: Output**
Save your final results to `/home/user/recommendations.json`. The file must be a standard JSON object mapping each target Product ID to its alphabetically sorted list of 3 recommended Product IDs.

Example output format:
```json
{
  "P001": ["P002", "P003", "P016"],
  "P005": ["P006", "P007", "P008"],
  "P009": ["P010", "P011", "P015"]
}
```
*(Note: The above is just a structural example, though it may closely resemble your final IDs).*