You are an MLOps engineer tasked with fixing an experiment tracking pipeline. A previous process dumped raw artifacts, but a misconfiguration caused downstream validation tools to fail because they were fed "blank" (all-zero or uninitialized) plots and embeddings. 

To fix this, you need to build a small ETL and validation tool in C that processes the raw binary embeddings, validates them numerically, joins them with metadata, and produces a clean CSV.

Your task:
1. Create a C program at `/home/user/src/etl_pipeline.c`.
2. The program must read two input files simultaneously:
   - `/home/user/data/embeddings.bin`: A binary file containing a sequence of 32-bit floating point vectors (each vector has a dimension of 4, little-endian).
   - `/home/user/data/metadata.txt`: A text file containing one string token per line, corresponding to the vectors in the binary file.
3. For each pair (vector, token) read from the sources, your program must:
   - Calculate the L2 norm (Euclidean length) of the vector.
   - **Numerical Testing:** If the L2 norm is `0.0`, the vector is an anomalous "blank" artifact. You must **skip** this vector and not write it to the output.
   - Normalize the vector (divide each of the 4 components by the L2 norm).
4. For valid vectors, append a row to a CSV file located at `/home/user/output/normalized_dataset.csv`.
5. The output CSV must have the following header:
   `id,token,e0,e1,e2,e3`
   Where `id` is the zero-based index of the vector from the original input files (e.g., if the 2nd vector is skipped, the output should show IDs `0` and `2`), `token` is the associated string, and `e0` through `e3` are the normalized float values printed with exactly 6 decimal places (e.g., `%0.6f`).

Once you have written `/home/user/src/etl_pipeline.c`, compile it using standard `gcc` (remember to link the math library if needed), and run it to generate `/home/user/output/normalized_dataset.csv`.