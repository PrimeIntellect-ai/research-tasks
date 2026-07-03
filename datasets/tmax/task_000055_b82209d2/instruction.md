I need you to prepare a robust training dataset from a recent experimental fluid dynamics run, and I'm running into severe numerical instability issues. 

We recorded a tracer particle experiment, and the video is located at `/app/particle_motion.mp4`. Your task involves a multi-stage workflow:

1. **Video Extraction & Data Prep:** 
   Extract the frame-by-frame 2D coordinates of the 5 brightest tracer particles in `/app/particle_motion.mp4`. Use standard techniques (e.g., `ffmpeg` for frame extraction, then OpenCV/SciPy in Python to find the local maxima). Save this raw trajectory data to `/home/user/trajectories.csv`.

2. **Covariance Estimation & MCMC:**
   Write a script that uses MCMC sampling to estimate the true underlying covariance matrix of these particle positions, assuming Gaussian noise. The raw empirical covariance matrix of these trajectories is highly ill-conditioned (near-singular) due to the particles frequently clustering and moving linearly in the flow.

3. **Robust Matrix Factorization Script:**
   I need you to write a standalone utility script at `/home/user/matrix_prep.py` that takes an input CSV representing *any* square matrix and performs a stabilized matrix factorization to generate training features. Because our data yields near-singular matrices, standard Cholesky or SVD fails or explodes.
   
   Your script `matrix_prep.py` must accept a single argument (the path to an input CSV containing a matrix) and print the stabilized, factorized matrix to standard output in comma-separated format. 
   
   To ensure your stabilization method perfectly matches our downstream ML pipeline's expectations, you must implement exactly the following regularization:
   - Compute the symmetric part of the input matrix: `A_sym = (A + A.T) / 2`.
   - Perform an eigenvalue decomposition.
   - For any eigenvalue less than `1e-5`, clip it exactly to `1e-5`.
   - Reconstruct the matrix: `A_reg = Q * Lambda_clipped * Q.T`.
   - Compute and print the Cholesky decomposition (lower triangular `L`) of `A_reg`.

You must create `/home/user/matrix_prep.py` such that it can perfectly handle any matrix provided to it using the exact clipping algorithm described. Run your script on the covariance matrix you estimated from the video to verify it works without crashing.