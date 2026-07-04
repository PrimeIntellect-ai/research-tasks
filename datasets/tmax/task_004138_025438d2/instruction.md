You are an ML systems engineer preparing a C-based high-performance data preparation pipeline. Before integrating the pipeline, you need to write a standalone C program to test the numerical accuracy of computing cosine similarities under simulated 8-bit quantization.

We have generated a dataset of embeddings located at `/home/user/embeddings.bin`.
- Format: Raw binary file containing exactly 100 vectors.
- Data type: `float32` (little-endian).
- Dimensions: Each vector has 64 dimensions.

Your task is to write a C program (save it anywhere, compile and run it) that does the following:
1. **Load the data**: Read the 100 vectors from `/home/user/embeddings.bin`. The first vector (index 0) is the "query" vector.
2. **Exact Cosine Similarity (Linear Algebra)**: For vectors 1 through 99, compute the exact cosine similarity against vector 0. 
   - Formula: `dot(A, B) / (norm(A) * norm(B))`
   - Perform all intermediate math for the similarity computation in `double` precision.
3. **Similarity Search**: Find the indices (1 to 99) of the top 3 vectors most similar to vector 0 based on the exact cosine similarity.
4. **Simulate Quantization**: Create a "quantized" version of all vectors using the formula: `q_val = round(val * 127.0) / 127.0`.
5. **Numerical Accuracy Test**: Compute the quantized cosine similarities between the quantized vector 0 and the quantized vectors 1 through 99.
6. **Hypothesis Testing (Confidence Intervals)**: 
   - Calculate the error for each vector $i \in [1, 99]$: `error_i = exact_sim_i - quantized_sim_i`
   - Compute the mean error across these 99 samples.
   - Compute the 95% Confidence Interval margin of error for the mean error.
   - Formula for margin of error: `1.96 * (sample_standard_deviation / sqrt(99))` (Ensure you use the sample standard deviation, dividing by N-1).

Once computed, output your results to a file named `/home/user/results.txt` with exactly the following format (ensure values are rounded to 6 decimal places):
```
Top3_Indices: A, B, C
Mean_Error: X.XXXXXX
CI_Margin: Y.XXXXXX
```
*(Where A, B, C are the integer indices ordered from most similar to least similar, and X/Y are your computed floating-point values).*