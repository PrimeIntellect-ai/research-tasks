You are a bioinformatics analyst studying the GC-content bias in specific genomic regions. You hypothesize that the GC-content distribution over a normalized genomic window `[0, 1]` is not uniformly distributed (the null model), but instead follows a position-dependent polynomial density gradient (the alternative model).

You need to write a C program, `/home/user/analyze_gc.c`, that estimates the alternative model's density, normalizes it, and performs a Likelihood Ratio Test (LRT) against the uniform null model.

Here are the specific steps your C program must perform:

1. **Matrix Decomposition / System Solving:** 
   Read a 3x4 augmented matrix from `/home/user/system.txt`. This matrix represents the normal equations derived from a Galerkin projection of the sequence data.
   Solve the linear system $M \mathbf{c} = \mathbf{y}$ for the coefficients $\mathbf{c} = [c_0, c_1, c_2]^T$ using an exact matrix decomposition or elimination method of your choice.
   These coefficients define the unnormalized polynomial density function: $f(x) = c_0 + c_1 x + c_2 x^2$.

2. **Numerical Integration:**
   Calculate the normalization constant $Z = \int_{0}^{1} f(x) dx$ to ensure the density is a valid probability distribution.
   You **must** calculate this integral numerically using **Simpson's 1/3 rule** with exactly $N=100$ subintervals (i.e., 101 evaluation points from 0.0 to 1.0).

3. **Density Estimation & Log-Likelihood:**
   Read a list of observed GC-content data points from `/home/user/gc_data.txt` (one float per line).
   For each point $x_i$, evaluate the normalized alternative probability density: $p_{alt}(x_i) = f(x_i) / Z$.
   Compute the alternative log-likelihood: $LL_{alt} = \sum_{i} \ln(p_{alt}(x_i))$.

4. **Statistical Hypothesis Comparison:**
   The null model assumes GC-content is strictly Uniform(0,1), so $p_{null}(x_i) = 1$ for all $x$, making the null log-likelihood $LL_{null} = 0$.
   Compute the Likelihood Ratio Test statistic: $LRT = 2 \times (LL_{alt} - LL_{null})$.

5. **Output:**
   Your program must write the single final LRT statistic value to `/home/user/lrt_result.txt`, formatted to exactly 5 decimal places (e.g., `1.23456`). Do not include any other text in this output file.

Compile and run your C program to produce the final output file. You may use standard C math libraries (remember to link with `-lm`).