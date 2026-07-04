You are an ML engineer preparing a preprocessing pipeline. We need to extract a rank-1 approximation of a dataset matrix ($A \approx u v^T$) using gradient descent, but our current implementation suffers from numerical instability (exploding gradients) on near-singular or poorly scaled inputs, and it's too slow.

In `/home/user/mf.cpp`, there is an incomplete C++ implementation of this gradient descent. 

Your task is to fix and optimize this code:
1. **Numerical Stability:** The current loss function is just the squared error: $L = \sum_{i,j} (A_{i,j} - u_i v_j)^2$. Modify the gradient calculations in the C++ code to include L2 regularization (Ridge penalty) to prevent the weights from exploding. The new objective should be: 
   $L = \sum_{i,j} (A_{i,j} - u_i v_j)^2 + \lambda (\sum_i u_i^2 + \sum_j v_j^2)$
   Use $\lambda = 0.05$. 
2. **Parallel Computing:** The matrix is large. Add OpenMP pragmas (`#pragma omp parallel for`) to parallelize the outer loops of the gradient computation for both $u$ and $v$.
3. **Compilation & Execution:** 
   - Compile the code using `g++` with OpenMP support (`-fopenmp`) and output the executable to `/home/user/mf`.
   - Run the executable on the provided dataset `/home/user/matrix.txt` with the environment variable `OMP_NUM_THREADS=4`.
   - The program will automatically write its output to `/home/user/final_loss.txt`.

Ensure your C++ code correctly calculates the regularized gradients:
- $\frac{\partial L}{\partial u_i} = \sum_j -2(A_{i,j} - u_i v_j)v_j + 2\lambda u_i$
- $\frac{\partial L}{\partial v_j} = \sum_i -2(A_{i,j} - u_i v_j)u_i + 2\lambda v_j$

The learning rate is pre-set to $0.001$, and the number of iterations to $100$. Leave these hyperparameters as they are in the starter code. Provide the final compiled binary and ensure `/home/user/final_loss.txt` is generated with the final regularized loss.