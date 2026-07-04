You are a machine learning engineer preparing a robust microservice to pre-compute regression weights for training data. 

We have a vendored C++ service located at `/app/ridge_solver` that performs parallelized 1D Ridge Regression (curve fitting for $y = w_1 x + w_0$). It calculates the analytical solution $w = (X^T X + \lambda I)^{-1} X^T y$.

However, the current implementation has a critical flaw: it fails or produces NaN values on near-singular inputs (e.g., when the feature variance is extremely low) because the C++ code has a bug in how it applies the regularization parameter $\lambda$. 

Your tasks are:
1. **Fix the C++ code:** Inspect and fix `/app/ridge_solver/src/solver.cpp`. The code calculates the 2x2 matrix $X^T X$ components (where `a = sum_x2`, `b = sum_x`, `c = sum_x`, `d = n`), but it fails to add the regularization parameter `lambda` to the diagonal elements (`a` and `d`) *before* calculating the determinant and the inverse. Update the code so that `lambda` is correctly added to `a` and `d`.
2. **Compile the scientific software:** Compile the fixed C++ code into an executable named `solver` inside the `/app/ridge_solver` directory. The code uses OpenMP for parallelizing the summations, so you must compile it with OpenMP support enabled (e.g., using `g++`).
3. **Start the service:** We have provided a Python HTTP wrapper `/app/ridge_solver/server.py` which takes the port as a command-line argument and calls your compiled `./solver`. Start this server so it listens on `127.0.0.1:8080`. Leave the server running in the background.

The API wrapper expects your C++ program to take arguments: `./solver <lambda> <csv_file_path>` and output a single line to stdout in the format: `w1=<value>,w0=<value>`. The wrapper then exposes an HTTP POST endpoint at `/fit`.

Please make the necessary code changes, compile the binary, and start the server on port 8080.