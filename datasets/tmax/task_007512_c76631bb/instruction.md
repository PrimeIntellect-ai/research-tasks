You are an ML engineer preparing graph training data for a molecular spectroscopy model. We use the graph Laplacian to compute a structural embedding matrix for the molecules.

In your workspace `/home/user`, there is a C++ source file `prep_data.cpp` that:
1. Simulates reading molecular spectroscopy signals (probability distributions over frequency bins) for 3 nodes.
2. Computes the Jensen-Shannon (JS) divergence between the spectra of connected nodes to use as edge weights.
3. Builds the graph Laplacian matrix $L = D - A$.
4. Attempts to compute the inverse of the Laplacian to generate the final dense training features, saving it to `/home/user/training_features.csv`.

However, the pipeline is currently broken:
- The required linear algebra library, Eigen3, is missing.
- When compiled and run with Eigen, the program outputs NaNs or garbage values because the standard graph Laplacian is singular (it has an eigenvalue of 0), causing the direct `.inverse()` matrix factorization to fail.

Your task:
1. Set up the scientific environment by downloading the Eigen source code (version 3.4.0) into `/home/user/eigen`. You can download it from `https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz` and extract it such that the headers are available at `/home/user/eigen/Eigen`.
2. Fix `prep_data.cpp` to prevent the singularity issue. Add a small Tikhonov regularization term to the Laplacian before inversion. Specifically, add $10^{-5} \times I$ (where $I$ is the identity matrix) to $L$ before computing the inverse.
3. Compile the C++ program using `g++` (ensure you include the Eigen directory with `-I/home/user/eigen`). Name the executable `prep_data`.
4. Run `./prep_data` to generate the corrected `/home/user/training_features.csv`.

The output `/home/user/training_features.csv` must contain the 3x3 regularized inverse Laplacian matrix, with comma-separated values.