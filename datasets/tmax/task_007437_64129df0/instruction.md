You are a data analyst tasked with building a quick product recommendation utility based on text embeddings. 

You have been provided with two datasets in your home directory:
1. `/home/user/products.csv` - Contains product metadata (`product_id`, `description`).
2. `/home/user/history.csv` - Contains user purchase history (`user_id`, `product_id`).

You also have a pre-trained feature extractor model saved as `/home/user/vectorizer.pkl`. This is a fitted `scikit-learn` `TfidfVectorizer` object.

Your objective is to write and run a Python script that completes the following steps:

1. **Environment Setup**: Ensure necessary packages like `pandas` and `scikit-learn` are installed.
2. **Data Filtering**: Identify all `product_id`s that `user_42` has interacted with in `history.csv`.
3. **Inference & Benchmarking**: 
   - Load the `/home/user/vectorizer.pkl` model.
   - Run inference (i.e., the `.transform()` method) on the `description` column of *all* products in `products.csv`. 
   - You must benchmark the performance of this specific inference step. Measure the time taken to execute the `.transform()` call.
   - Save the elapsed time in seconds (as a simple float, e.g., `0.0045`) to a file named `/home/user/inference_time.txt`.
4. **Similarity Search**: 
   - Calculate the cosine similarity between the product vectors.
   - For each product that `user_42` interacted with, find the *single most similar* product in the entire catalog based on the computed cosine similarity.
   - You cannot recommend the product itself. 
   - If there is a tie in similarity scores, pick the product with the alphanumerically smaller `product_id`.
5. **Reporting**: 
   - Save your final recommendations to `/home/user/recommendations.csv`.
   - The CSV must have exactly two columns: `original_product_id` and `recommended_product_id`.
   - Sort the rows alphanumerically by `original_product_id`.

Please execute your workflow and leave the requested output files (`inference_time.txt` and `recommendations.csv`) in `/home/user/`.