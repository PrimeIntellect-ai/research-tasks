You are a data scientist building a custom ETL and data cleaning pipeline in Rust. You have a dirty dataset of e-commerce product listings at `/home/user/raw_products.csv`. Some products are duplicates, and some have missing prices. You need to write a Rust program to clean the data, find duplicates using similarity search, and impute missing prices using a custom k-Nearest Neighbors (KNN) regressor with hyperparameters tuned via cross-validation.

Here is the format of `/home/user/raw_products.csv`:
```csv
id,description,price
1,red mechanical keyboard cherry mx,100.0
2,red mechanical keyboard cherry mx switch,105.0
...
```
Prices can be empty (e.g., `5,wireless optical mouse ergonomic,`).

Please create a Rust project in `/home/user/pipeline` and write a program that does the following:

1. **ETL & Preprocessing:**
   - Read `/home/user/raw_products.csv`.
   - Tokenize the descriptions by lowercasing them and splitting by whitespace.

2. **Similarity Search (Deduplication):**
   - Compute the Jaccard similarity between all pairs of products. Jaccard similarity is the size of the intersection of tokens divided by the size of the union of tokens.
   - Find all pairs of products where the Jaccard similarity is strictly greater than `0.75`.
   - Output these duplicate pairs to `/home/user/duplicates.csv` with columns `id1,id2`. Ensure `id1 < id2` for each pair, and sort the rows by `id1` ascending, then `id2` ascending.

3. **Hyperparameter Tuning (Cross-Validation for KNN Regression):**
   - You need to build a KNN regressor to predict missing prices based on description similarity. 
   - The price is predicted as the arithmetic mean of the prices of the $K$ most similar items (using Jaccard similarity). If there is a tie in similarity, prioritize the item with the smaller `id`.
   - To find the best $K$, perform Leave-One-Out Cross-Validation (LOOCV) *only* on the subset of items that already have a price. 
   - For each item with a known price, temporarily remove it from the known set, find its $K$ nearest neighbors in the remaining known set, and predict its price.
   - Compute the Mean Absolute Error (MAE) for $K \in \{1, 2, 3\}$.
   - Select the $K$ that yields the lowest MAE. If there is a tie in MAE, pick the smaller $K$.

4. **Imputation & Export:**
   - Using the best $K$ found above, predict the missing prices in the dataset by finding the $K$ nearest neighbors from the set of items with *known* prices.
   - Write the fully cleaned dataset (original known prices + imputed prices) to `/home/user/cleaned_products.csv` with columns `id,description,price`.
   - Format the prices to exactly 2 decimal places (e.g., `100.00`). Sort the output by `id` ascending.

Requirements:
- You must write the solution in Rust inside `/home/user/pipeline`. You can use external crates like `csv` and `serde` (you will need to run `cargo init` and `cargo add` as appropriate).
- Compile and run your Rust program so that it produces the two output CSV files.