You are acting as a data scientist setting up a reproducible curve-fitting pipeline. 

We have a set of experimental observations located at `/home/user/dataset.csv`. The file has two columns, `x` and `y`, with headers. 
You need to fit a quadratic polynomial regression model to this data: 
$y = c_0 + c_1 x + c_2 x^2$

Your task is to:
1. Initialize a new Rust project named `polyfit` in `/home/user/polyfit`.
2. Write a Rust program in this project that reads `/home/user/dataset.csv`.
3. Construct the design matrix $A$ for the quadratic model and the observation vector $y$.
4. Use a matrix decomposition technique (e.g., QR, SVD, or Cholesky) to solve the linear least-squares problem for the coefficients $(c_0, c_1, c_2)$. (I recommend using the pure-Rust `nalgebra` crate to avoid external C-library dependencies).
5. Output the computed coefficients as a simple JSON array `[c_0, c_1, c_2]` and save it to `/home/user/result.json`.
6. Create a reproducible bash script at `/home/user/pipeline.sh` that compiles the Rust project in release mode and executes the binary to produce the `result.json` file. Ensure the script has executable permissions.

Do not use any external solvers or CLI curve-fitting tools; the matrix decomposition and least-squares solve must be explicitly performed in your compiled Rust code.