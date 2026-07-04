You are a performance engineer tasked with implementing a highly stable numerical solver. Our current simulation produces non-reproducible results across different nodes due to floating-point reduction order differences during large summations.

Your task is to write a C program that computes a solution to a linear system, maps it to a probability distribution, and calculates its distance to a reference distribution, while strictly controlling floating-point errors.

Write a C program at `/home/user/solve_and_compare.c` that does the following:
1. Reads a 100x100 matrix $A$ from `/home/user/matrix_A.bin`. The file contains 10000 64-bit IEEE 754 floating-point numbers (double precision) in row-major order.
2. Reads a 100-element vector $b$ from `/home/user/vector_b.bin` (double precision).
3. Reads a 100-element vector $q$ from `/home/user/vector_q.bin` (double precision). This is a reference probability distribution.
4. Computes the **Cholesky decomposition** of $A$ ($A = L L^T$). You may assume $A$ is symmetric positive-definite.
5. Solves the linear system $A x = b$ for $x$ using forward and backward substitution with the Cholesky factor $L$.
6. Converts the resulting vector $x$ into a probability distribution $p$ using the **softmax** function: $p_i = \frac{e^{x_i}}{\sum_{j=1}^{100} e^{x_j}}$.
7. Computes the Kullback-Leibler (KL) divergence from $q$ to $p$: $D_{KL}(p \parallel q) = \sum_{i=1}^{100} p_i \ln\left(\frac{p_i}{q_i}\right)$.
8. **Crucial:** To fix the non-reproducibility issues, you **must** use the **Kahan summation algorithm** when computing the sum for the softmax denominator and the sum for the KL divergence.
9. Prints the final KL divergence to standard output, formatted to exactly 15 decimal places (e.g., `printf("%.15f\n", kl);`).

Once your code is written:
- Compile it with `gcc -O3 solve_and_compare.c -o solve_and_compare -lm`.
- Run it and redirect the output to `/home/user/kl_result.txt`.

Ensure your code handles file reading and basic memory management correctly. There are no missing values or NaNs in the inputs.