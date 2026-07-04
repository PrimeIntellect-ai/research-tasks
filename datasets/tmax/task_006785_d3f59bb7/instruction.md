You are an ML Engineer preparing a representative centroid for a large dataset of embeddings to use in a similarity search application. 

You have a dataset of 100,000 embeddings, each of dimension 16 (stored as 32-bit floats), located at `/home/user/embeddings.bin`. The file contains no header, just raw binary float data (100,000 * 16 * 4 bytes).

Your task is to write a C program `/home/user/process_embeddings.c` that performs bootstrap sampling to estimate the robust centroid of the embeddings, finds the nearest neighbors to this centroid, and benchmarks the search performance.

The program must implement the following steps:
1. **Load Data:** Read the 100,000 vectors from `/home/user/embeddings.bin`.
2. **Bootstrap Centroid Estimation:** 
   - Perform 100 bootstrap iterations.
   - In each iteration, sample 100,000 vector indices with replacement.
   - Calculate the mean vector for the sample.
   - The final `bootstrapped_centroid` is the average of the 100 mean vectors.
   - *Important:* To ensure reproducibility, use the following simple LCG for random number generation instead of `rand()`. Initialize `uint32_t state = 42;` once at the very beginning of the program, before the outer loop.
     ```c
     uint32_t next_rand() {
         state = state * 1664525 + 1013904223;
         return state;
     }
     ```
     To sample an index, use `next_rand() % 100000`.
3. **Similarity Search & Benchmarking:**
   - Record the start time (using `clock_gettime` or `gettimeofday`).
   - Perform a linear scan to find the 5 vectors in the entire dataset that are closest to the `bootstrapped_centroid` using Euclidean distance.
   - Record the end time and calculate the search duration in microseconds.
4. **Output:** 
   - Write the results to a file named `/home/user/results.log` in the exact format shown below. The centroid coordinates should be formatted to 3 decimal places (`%.3f`). The closest indices must be sorted from closest (smallest distance) to furthest.

Example `/home/user/results.log` format:
```
Centroid: 0.123 -0.456 0.789 ... [all 16 values separated by space]
Closest Indices: 12, 45, 999, 1234, 5678
Search Time: 450 us
```

After writing the C program, compile it with `gcc -O3 process_embeddings.c -o process_embeddings -lm` and run it to produce `/home/user/results.log`.