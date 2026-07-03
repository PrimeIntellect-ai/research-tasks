You are acting as a research assistant for a computational materials scientist. They are running large-scale numerical simulations that output stress-energy covariance matrices. Unfortunately, numerical instabilities in the upstream PDE solver occasionally produce physically invalid (non-symmetric or non-positive-definite) matrices.

You have three main objectives:

1. **Fix and Install a Vendored Package**:
   The lab uses a custom, highly optimized package called `fast_svd_custom` for matrix decompositions. The source code for version `0.1.0` is vendored at `/app/fast_svd_custom-0.1.0`. However, the installation (`pip install .`) currently fails due to a deliberate perturbation/bug in the package's build configuration. 
   - Identify the bug preventing installation. Fix it.
   - Run the package's regression tests (`pytest tests/`) to ensure the matrix decomposition routines are working correctly.
   - Install the package into your Python environment.

2. **Create a Matrix Sanitizer (Adversarial Filter)**:
   You need to write a classifier script at `/home/user/detector.py` that uses the installed `fast_svd_custom` library to detect whether a given `.npy` file containing a 2D matrix is physically valid ("clean") or corrupted ("evil").
   - A matrix is "CLEAN" if it is strictly symmetric (tolerance $10^{-5}$) and positive definite (all eigenvalues > 0).
   - A matrix is "EVIL" if it is asymmetric or contains negative eigenvalues.
   - Your script must take exactly one positional argument: the path to a `.npy` file.
   - It must print exactly `CLEAN` to standard output if the matrix is valid, and exactly `EVIL` if it is corrupted. It must exit with code 0 in both cases.

3. **Data Visualization**:
   Write a script at `/home/user/visualize.py` that loads a directory of `.npy` matrices (passed via `--dir` argument), computes their Singular Value Decomposition (SVD), and creates a 2D scatter plot of the First Singular Value (X-axis) versus the Second Singular Value (Y-axis).
   - Save the plot as an image at `/home/user/svd_plot.png`.

Ensure your implementations are robust. An automated grading script will run your `detector.py` against a hidden corpus of clean and evil matrix files to verify your classifier.