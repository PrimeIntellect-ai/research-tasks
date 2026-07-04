You are a data scientist preparing feature embeddings for a lightweight inference engine. You have a messy dataset at `/home/user/embeddings.csv`.

Your task is to:
1. Clean and aggregate the dataset using shell utilities. The CSV has the format `category,v1,v2,v3`. Some rows are corrupted (e.g., contain non-numeric data in the vector columns or have missing columns). Filter out the invalid rows. 
2. For each `category`, calculate the mean of `v1`, `v2`, and `v3` across all valid rows.
3. Write a Rust program at `/home/user/inference.rs` that:
   - Reads the aggregated category means.
   - Computes the dot product of each category's mean vector with the fixed weight vector `W = [0.25, 0.5, -0.25]`.
   - Simulates an inference benchmark by running this dot product calculation 1,000,000 times in a loop (to measure optimization performance) and prints the elapsed time to stdout.
   - Finds the category with the highest resulting dot product score.
4. The Rust program must write the name of the winning category and its exact score (formatted to 4 decimal places) to `/home/user/best_category.txt` in the format: `CategoryName,Score`.

Compile your Rust program using `rustc /home/user/inference.rs -O` and run it to produce the final output.