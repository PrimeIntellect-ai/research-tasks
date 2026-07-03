You are assisting a data scientist fitting a spatial probability model. 

There is a C program located at `/home/user/fit_model.c` that evaluates a probability density function over a 1D spatial domain `[-5, 5]`. The domain is decomposed into a mesh of `N` equal intervals (where `N` is provided as a command-line argument). The program computes the discrete probability mass across the mesh, normalizes it, and calculates the L1 distance (Total Variation) against the known analytical solution to validate the model.

Currently, the model passes validation for coarse meshes, but fails due to a numerical stability issue upon severe mesh refinement. When `N` is very large (e.g., 10,000,000), accumulating the sum of millions of tiny interval probabilities into a single precision `float` accumulator causes catastrophic precision loss, making the normalization constant incorrect and severely skewing the resulting distribution distance metric.

Your task:
1. Identify the precision issue in `/home/user/fit_model.c`. Modify the code to use double-precision (`double`) for the probability accumulator (`total_prob`) and the values array (`p_vals`).
2. Compile the scientific software from source using `gcc -O2 fit_model.c -o fit_model -lm`.
3. Run the compiled tool to calculate the probability distribution distance metric for two mesh refinement levels: `N = 1000` and `N = 10000000`.
4. Create a log file at `/home/user/results.txt` containing exactly two lines. The first line should be the program's output for `N = 1000`, and the second line should be the output for `N = 10000000`. 

Ensure that your final `results.txt` strictly contains the two floating-point outputs.