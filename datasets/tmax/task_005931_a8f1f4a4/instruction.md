I am a data analyst working on a small recommendation system. I have a set of item embeddings in a CSV file, but our previous pipeline kept producing blank arrays and NaN values due to a backend misconfiguration when applying our transformation model. 

I need you to write a fresh C program from scratch that acts as an end-to-end ETL pipeline, applies a simple reconstructed model transformation, and performs a similarity search to recommend the best items.

Here is the setup:
You are provided with three files in the `/home/user/data/` directory (you will need to create this directory and the files for testing, but assume they exist in production):
1. `items.csv`: Contains item features. Each row is `id,f1,f2,f3,f4`. (ID is an integer, f1-f4 are floats).
2. `weights.csv`: Contains a 4x4 transformation matrix (4 rows, 4 comma-separated floats per row). This represents our model's dense layer.
3. `target.csv`: Contains a single row of 4 comma-separated floats `f1,f2,f3,f4`. This is the user's current context vector.

Your C program must:
1. Parse all three CSV files.
2. Apply the transformation matrix to each item vector and to the target vector. The transformation is a standard matrix-vector multiplication: `v_out = W * v_in`, where `W` is the 4x4 weight matrix and `v_in` is the 4x1 feature column vector.
3. Compute the Cosine Similarity between the transformed target vector and every transformed item vector.
4. Find the top 3 items with the highest cosine similarity to the target vector.
5. Write the integer IDs of these top 3 items to `/home/user/recommendations.txt`, with one ID per line, sorted from highest similarity to lowest.

Requirements:
- Write your C code in `/home/user/recommend.c`.
- Compile it to `/home/user/recommend` using `gcc -O2 -lm recommend.c -o recommend`.
- Run the executable to produce the output file.
- Handle potential floating-point edge cases (e.g., zero magnitude vectors should have a similarity of 0).