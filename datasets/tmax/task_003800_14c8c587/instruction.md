You are a data engineer tasked with building an ETL (Extract, Transform, Load) pipeline that processes a messy inventory dataset, engineers new features, handles anomalies, and computes semantic embeddings for product search. 

Your goal is to write a pipeline consisting of a bash script (`/home/user/run_pipeline.sh`) that orchestrates Python data processing.

**Input Data:**
You are provided with a raw dataset at `/home/user/inventory.csv`. The columns are:
`id`, `product_name`, `price`, `weight`, `length`, `width`, `height`.

**Pipeline Requirements:**

1. **Missing Value Handling:**
   - Impute missing `price` values with the median `price` of the dataset.
   - Impute missing `weight` values with the mean `weight` of the dataset.
   - Any rows missing `length`, `width`, or `height` should be dropped entirely.

2. **Feature Engineering:**
   - Create a new feature called `volume` calculated as `length * width * height`.
   - Create a new feature called `density` calculated as `weight / volume`.

3. **Outlier Removal:**
   - Calculate the Z-score of the `density` column.
   - Remove any rows where the `density` has a Z-score absolute value strictly greater than 2.0. (Use sample standard deviation).

4. **Embedding Computation:**
   - Install the `sentence-transformers` library.
   - Use the pre-trained model `all-MiniLM-L6-v2` to compute embeddings for the `product_name` of all remaining rows.
   
5. **Retrieval & Output:**
   - After cleaning and processing, save the cleaned dataset (including `volume` and `density`, but excluding the embeddings array to save space) as a JSON Lines file to `/home/user/cleaned_inventory.jsonl`.
   - Calculate the cosine similarity between all cleaned product name embeddings and the embedding for the search query: `"Heavy duty industrial steel storage rack"`.
   - Find the `id` of the single product with the highest cosine similarity to the query. Write ONLY this integer `id` to the file `/home/user/best_match.txt`.

**Execution:**
Ensure your solution can be run end-to-end simply by executing `bash /home/user/run_pipeline.sh`. The pipeline should install any necessary dependencies (like pandas, scikit-learn, sentence-transformers) locally if they are not present.