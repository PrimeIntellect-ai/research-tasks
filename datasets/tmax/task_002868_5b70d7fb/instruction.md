You are an AI assistant helping a data scientist clean a dataset using a custom, high-performance C++ pipeline. We are working with text data, and we need to filter out near-duplicates using a custom embedding approach to simulate a semantic retrieval and filtering process.

Your objective is to build a reproducible C++ pipeline that reads text data, computes a simulated embedding, performs a similarity search to find near-duplicates, filters them out, and benchmarks the inference/processing performance.

Here are the specific requirements:

1. **Environment & Files**:
   - The raw data is located at `/home/user/data/raw_dataset.txt` (each line is a separate document).
   - You need to write your C++ code to `/home/user/cleaner.cpp`.
   - You must write a Makefile at `/home/user/Makefile` that compiles the code into an executable named `cleaner` using the `-O3` optimization flag.
   - Output the filtered lines to `/home/user/data/cleaned_dataset.txt`.
   - Output benchmark metrics to `/home/user/data/benchmark.json`.

2. **Custom Embedding & Retrieval Logic**:
   - For each line (document) in the raw dataset, compute a 16-dimensional embedding.
   - **Embedding Algorithm**: 
     - Initialize a 16-element float array `vec` to zeros.
     - For each character `c` in the string (including spaces, using its ASCII value), and for each dimension `i` from 0 to 15, add `(int(c) * (i + 1))` to an accumulator.
     - After summing over all characters, `vec[i]` is the accumulator modulo 100 (i.e., `vec[i] = sum % 100`).
     - Finally, L2-normalize the vector. (Compute the Euclidean norm. If the norm is > 0, divide each element by the norm. If the norm is 0, leave it as 0).
   - **Filtering (Retrieval)**:
     - Keep track of the embeddings of all "accepted" lines.
     - For each new line, compute the cosine similarity (which is just the dot product of the L2-normalized vectors) against all previously accepted lines.
     - If the maximum similarity to any accepted line is **>= 0.90**, consider it a near-duplicate and discard it.
     - If it is < 0.90 (or if there are no accepted lines yet), accept the line, output it to the cleaned dataset, and add its embedding to the accepted list.
     - Process the lines strictly in the order they appear in `raw_dataset.txt`.

3. **Performance Benchmarking**:
   - Time *only* the dataset processing phase (from opening the input file and starting the computation to closing the output file).
   - After processing, your C++ program must write a JSON file to `/home/user/data/benchmark.json` with the following exact format:
     `{"total_lines": <integer>, "kept_lines": <integer>, "time_seconds": <float>, "throughput_lines_per_sec": <float>}`

4. **Reproducible Pipeline construction**:
   - Create a shell script at `/home/user/run_pipeline.sh`.
   - This script should:
     - Invoke `make` to build the `cleaner` binary.
     - Execute `./cleaner`.
     - Compute the SHA-256 checksum of `/home/user/data/cleaned_dataset.txt` and save just the hash (the first field of the `sha256sum` output) to `/home/user/data/reproducibility_hash.txt`.

Ensure the script is executable and the paths are exactly as specified.