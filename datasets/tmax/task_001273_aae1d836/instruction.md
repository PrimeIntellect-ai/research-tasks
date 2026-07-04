You are an AI assistant helping a data scientist clean a dataset using high-performance C code. 

We have a dataset of product embeddings located at `/home/user/data/embeddings.csv`. The file does not have a header. Each line is supposed to contain a product ID (an integer) followed by exactly 16 floating-point numbers representing the embedding vector. The values are comma-separated.

Unfortunately, the dataset is messy. Some rows are malformed (e.g., wrong number of columns, non-numeric values where floats or ints are expected). Furthermore, we suspect there are near-duplicate products in the dataset.

Your task is to write a C program that performs data cleaning, similarity search, and benchmarking. 

Please perform the following steps:
1. Create a directory `/home/user/src/` and write your C code to `/home/user/src/cleaner.c`.
2. Create a directory `/home/user/bin/` and compile your code to `/home/user/bin/cleaner` (use `-O3` and link the math library `-lm`).
3. Create a directory `/home/user/output/` where the program will write its results.

The C program must do the following when executed:
1. **Data Schema Enforcement:** Read `/home/user/data/embeddings.csv`. For each line, validate that it has exactly 1 integer ID and exactly 16 floating-point numbers. If a line is malformed or has parsing errors, write the exact raw line (including the original newline) to `/home/user/output/rejected.log` and exclude it from further processing.
2. **Embedding Computation & Similarity Search:** For all valid records, compute the pairwise Cosine Similarity between every unique pair of embeddings. Identify all pairs where the Cosine Similarity is greater than or equal to `0.9500`.
3. **Output Deduplication:** Write the near-duplicate pairs to `/home/user/output/duplicates.csv` in the format `id1,id2,similarity`. Ensure that `id1 < id2` for every pair. Sort the output rows primarily by `id1` ascending, and secondarily by `id2` ascending. Format the similarity to exactly 4 decimal places (e.g., `0.9812`).
4. **Inference Performance Benchmarking:** Wrap the pairwise similarity search portion of your code (the loops where the math happens, excluding file I/O) with timing code (e.g., using `clock_gettime`). Write the elapsed time to `/home/user/output/benchmark.txt` in the exact format: `Search took X.XXXXXX seconds.` (where X.XXXXXX is the time formatted to 6 decimal places).

Run your compiled program so that the output files are generated.