You are assisting a computational physics researcher analyzing structural vibrations from high-speed camera footage. The analysis pipeline uses Dynamic Mode Decomposition (DMD) to extract the primary modes of vibration. However, the automated pipeline often crashes because varying lighting or corrupted frames produce near-singular or ill-conditioned matrices that fail standard decomposition algorithms and subsequent numerical integration steps.

Your objective has two main parts:

**Part 1: Video Analysis and Stabilized DMD**
We have a test video located at `/app/vibration_test.mp4`. 
1. Extract the first 50 frames of this video as grayscale images at a resolution of 128x128 pixels.
2. Flatten each frame into a 1D column vector (length 16384).
3. Form two data matrices: 
   - $X_1$: containing frames 0 to 48 (columns).
   - $X_2$: containing frames 1 to 49 (columns).
4. Perform Dynamic Mode Decomposition to find the leading eigenvalues of the best-fit linear operator $A$ where $X_2 \approx A X_1$.
   - Because $X_1$ is highly ill-conditioned, you must use a truncated Singular Value Decomposition (SVD) keeping only the top $r=5$ singular values to compute the pseudo-inverse.
   - Calculate the discrete-time eigenvalues $\lambda$ of the reduced operator.
   - Convert these to continuous-time eigenvalues $\omega$ using the relation $\lambda = e^{\omega \Delta t}$, assuming a time step of $\Delta t = 0.01$ seconds.
5. Identify the top 3 continuous-time eigenvalues ($\omega$) sorted by their absolute magnitude in descending order.
6. Write these top 3 eigenvalues to `/home/user/dmd_eigenvalues.csv` in the exact format: `Rank,Real,Imaginary` (one header line, followed by the 3 rows).

**Part 2: Matrix Stability Filter**
The researcher wants to pre-filter matrices before they reach the fragile ODE solvers downstream. You must create a numerical stability sanitization script.
1. Write a Python script at `/home/user/matrix_filter.py`.
2. The script must accept exactly one command-line argument: the absolute path to a NumPy `.npy` file containing a 2D matrix.
3. The script must load the matrix and evaluate its numerical stability. It should reject the matrix if it is near-singular, highly ill-conditioned (Condition Number > $10^8$), or contains invalid entries (NaNs, Infs).
4. The script must terminate with:
   - **Exit code 0**: if the matrix is "clean" (well-conditioned and numerically stable).
   - **Exit code 1**: if the matrix is "evil" (fails the stability criteria).

Your filter will be tested against a hidden evaluation suite of clean and evil matrices.

Ensure all outputs strictly follow the requested paths and formats. You may use any standard Python scientific libraries (numpy, scipy, cv2) and system tools (ffmpeg) available.