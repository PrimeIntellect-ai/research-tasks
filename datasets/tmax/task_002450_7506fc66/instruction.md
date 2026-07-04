You are a data engineer building an ETL pipeline. As part of a legacy system migration, you need to implement a data transformation and retrieval step in C to maximize performance. 

You have been provided with three CSV files in your home directory `/home/user`:
- `input.csv`: Contains 100 rows, each with 10 floating-point numbers (your raw data).
- `weights.csv`: Contains 10 rows, each with 3 floating-point numbers (a linear projection matrix).
- `bias.csv`: Contains 1 row with 3 floating-point numbers.

Your task is to write a C program (e.g., `pipeline.c`) that performs the following steps:
1. **Model Architecture Reconstruction & Dimensionality Reduction**: Read the data. For each 10-dimensional input vector $x$, compute the 3-dimensional transformed vector $z$ using the linear layer transformation: $z = x W + b$, where $W$ is the weights matrix and $b$ is the bias vector.
2. **Embedding Computation**: Apply a ReLU activation function to $z$ (i.e., replace any negative value with 0) to get the final 3-dimensional embedding for each row.
3. **Retrieval**: Let $E_0$ be the final 3-dimensional embedding of the very first row (index 0) in `input.csv`. Compute the Euclidean distance between $E_0$ and the embeddings of all other rows.
4. **Reporting**: Find the 5 closest rows to row 0 (excluding row 0 itself) based on this Euclidean distance. Output their 0-based original row indices to a file named `/home/user/top5.txt`, writing one index per line, sorted from closest to furthest.

Constraints & Requirements:
- Use standard C libraries (e.g., `<stdio.h>`, `<stdlib.h>`, `<math.h>`, `<string.h>`).
- Compile your code using `gcc` and run it to produce the `top5.txt` file.
- The output file `/home/user/top5.txt` must contain exactly 5 lines, each containing a single integer.