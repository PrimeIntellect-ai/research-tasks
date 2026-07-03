You are an MLOps engineer tracking experiment artifacts. We are investigating whether we can apply dimensionality reduction to our embedding generation pipeline by identifying highly correlated embedding components across different models. 

You have two binary artifact files representing model embeddings extracted from a recent cross-validation run:
- `/home/user/artifacts/emb1.bin`
- `/home/user/artifacts/emb2.bin`

Each file contains exactly 1000 single-precision (32-bit) IEEE 754 floats.

We have a C program skeleton located at `/home/user/calc_corr.c` designed to compute the Pearson correlation coefficient between these two embedding vectors. However, the core mathematical function `compute_pearson` is incomplete and currently returns `0.0`.

Your task:
1. Edit `/home/user/calc_corr.c` to correctly implement the `compute_pearson(float* x, float* y, int n)` function. It should calculate and return the Pearson correlation coefficient between the two arrays.
2. Compile the C program. You can name the executable whatever you like, but make sure to link the math library (e.g., `-lm`).
3. Run the compiled executable, passing the two embedding files and the number of elements (1000) as arguments: `./<your_executable> /home/user/artifacts/emb1.bin /home/user/artifacts/emb2.bin 1000`.
4. Redirect the standard output of your program to `/home/user/corr_result.txt`.

The existing `main` function already handles reading the binary files and printing the result to 4 decimal places. You only need to implement the math logic in `compute_pearson`, compile, and run it.