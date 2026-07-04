You are a data engineer tasked with migrating and optimizing a legacy product recommendation pipeline.

We have a legacy feature extraction tool located at `/app/feature_extractor`. It is a compiled, stripped binary that takes text data and outputs dense embeddings. Your goal is to build an ETL pipeline that prepares the data, uses this black-box binary to generate embeddings, and implements a highly optimized similarity search script in Python.

Here are the specific requirements:

1. **Multi-Source Data Joining**:
   In `/home/user/data/`, you will find two files:
   - `products.csv`: Contains `product_id`, `name`, and `category`.
   - `descriptions.json`: A JSON lines file containing `{"id": <product_id>, "desc": "<description text>"}`.
   Write a script to join these sources. For each product, create a combined text string formatted exactly as: `[<category>] <name> - <desc>`. Ensure data is sorted numerically by `product_id` in ascending order.

2. **Feature Extraction via Legacy Binary**:
   The stripped binary `/app/feature_extractor` reads line-delimited text from standard input and outputs raw binary data to standard output. 
   - Each input line produces exactly one 64-dimensional dense vector of IEEE 754 single-precision floats (little-endian).
   - Use this binary to process your joined text data. Since calling the binary for each query in production is too slow, your ETL process must batch-process all products and serialize the resulting embeddings into an efficient format (e.g., a NumPy `.npy` file or a FAISS index) stored at `/home/user/embeddings.npy` (or `.index`).

3. **Optimized Similarity Search**:
   Create a Python script at `/home/user/recommend.py` that takes a `product_id` as a command-line argument and prints the `product_id`s of the top 10 most similar products (excluding the query product itself) based on Cosine Similarity.
   - The output must be exactly 10 comma-separated integers on a single line (e.g., `45,12,89,102,...`).
   - The script must load the precomputed embeddings and execute the search very quickly.

4. **Environment Setup**:
   You may install any necessary Python libraries (like `numpy`, `pandas`, `scipy`, `faiss-cpu`) using `pip` to accomplish this.

Your final deliverable (`/home/user/recommend.py`) will be benchmarked for both **inference performance** (execution time must be under 0.5 seconds per query) and **numerical accuracy** (the retrieved IDs must exactly match the true top-10 cosine similarity results derived from the binary's output).