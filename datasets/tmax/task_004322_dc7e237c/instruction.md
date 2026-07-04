You are an ML engineer preparing a training dataset for a physics-informed neural network. The pipeline relies on matrix factorization (Cholesky/SVD) of local deformation tensors, but it frequently fails due to numerical instability when encountering near-singular (ill-conditioned) inputs from the sensors. 

Your goal is to build a robust C-based sanitizer to filter out these "evil" near-singular matrices and process a raw video feed of new sensor data.

**Part 1: The Matrix Sanitizer (Adversarial Corpus)**
Write a C program that reads a square matrix from a text file and determines if it is well-conditioned ("clean") or near-singular ("evil").
- The text file contains the matrix size `N` on the first line, followed by `N` lines containing `N` floating-point numbers each.
- Standard deterministic decompositions (like full SVD) are too slow for our full pipeline. You MUST implement a **Monte Carlo** approach to estimate numerical stability (for example, using randomized power iteration to estimate the largest and smallest eigenvalues, testing convergence rates, or Hutchinson's trace estimation for the inverse). 
- Use **OpenMP** to parallelize the Monte Carlo trials or matrix-vector multiplications.
- Compile your program to `/home/user/sanitizer`.
- It should be invokable as: `/home/user/sanitizer <path_to_matrix_file>`
- **Exit codes:** Return `0` if the matrix is numerically stable (clean) and should be preserved. Return `1` if the matrix is near-singular/ill-conditioned (evil) and should be rejected.
- You are provided with a small sample of training data in `/app/sample_data/` to test your heuristics, but the automated verification will grade your compiled `/home/user/sanitizer` against a hidden adversarial corpus.

**Part 2: Processing the Sensor Video**
We also have a raw data feed exported as a video file at `/app/sensor_feed.mp4`. Each frame of this video represents a 100x100 grayscale matrix (1 pixel = 1 matrix element, where pixel value 0 represents 0.0 and 255 represents 1.0).
1. Extract all frames from `/app/sensor_feed.mp4`.
2. Convert each frame into the `N`x`N` text format described in Part 1 (where `N=100`).
3. Run your `/home/user/sanitizer` on every extracted frame.
4. Count the number of frames that are deemed "clean" (exit code 0).
5. Write this integer count to `/home/user/clean_frame_count.txt`.

Ensure your C code is numerically robust, avoids integer overflows in large files, and correctly uses parallel computing directives.