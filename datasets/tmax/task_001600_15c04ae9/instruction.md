You are a machine learning engineer tasked with optimizing the data preparation pipeline for a dense retrieval model. To maximize throughput, we need to move the embedding normalization and nearest-neighbor retrieval out of Python and into a highly optimized C program.

You have been provided with two binary files containing raw float32 embeddings (little-endian, IEEE 754):
1. `/home/user/base_embeddings.bin`: Contains 1000 vectors of dimension 64.
2. `/home/user/query_embeddings.bin`: Contains 50 query vectors of dimension 64.

Your task is to write a C program at `/home/user/embed_prep.c` that does the following:
1. Reads both binary files into memory.
2. L2-normalizes every vector in both sets (if a vector's norm is exactly 0, leave it as 0).
3. Benches the retrieval process: Start a timer using `clock()` right before the search loop, and stop it immediately after.
4. For each query vector, compute the cosine similarity (which is just the dot product of the L2-normalized vectors) against all base vectors to find the nearest neighbor (highest similarity).
5. Writes the results to `/home/user/nearest_neighbors.csv` with the exact header `query_id,nearest_base_id,cosine_similarity`. The similarity must be formatted to 4 decimal places (using `%.4f`). `query_id` and `nearest_base_id` are 0-indexed integers.
6. Writes the benchmarking result to `/home/user/benchmark.txt` in the format: `Search time: [X.XXXXXX] seconds` (using `%f` for the calculated seconds).

Requirements:
- Only standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `time.h`, etc.) are allowed.
- Compile your program with `gcc -O3 -lm embed_prep.c -o embed_prep` and run it.
- Ensure the output CSV perfectly matches standard formatting so our automated pipeline can parse it.