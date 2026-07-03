You are a data scientist working on fitting a relationship model between the topological structure of molecules and their spectroscopic signals. You have been given a dataset of graphs (representing molecules) and their noisy raw signals. 

Your objective is to process the graphs, denoise the signals, filter out numerically unstable/invalid molecules using a reference dataset, and fit a linear model.

All your work should be done in the `/home/user/spectro_graphs` directory. 

Here are the specific steps you must follow:

1. **Reference Dataset Comparison**:
   You have a file `/home/user/spectro_graphs/reference.csv` containing a list of `id`s representing structurally stable molecules. You must only process molecules whose `id` appears in this file. Ignore all others.

2. **Graph Algorithm (Topological Feature)**:
   The molecules are provided in `/home/user/spectro_graphs/molecules.json`. This file contains a list of dictionaries, each with an `id`, an `adjacency_matrix` (2D list representing an undirected, unweighted graph), and a `raw_signal` (list of 1024 floats).
   For each valid molecule, compute its **Wiener Index** ($W$). The Wiener Index is defined as the sum of the shortest path distances between all pairs of distinct nodes $i, j$ (where $i < j$). You may assume all valid molecular graphs are fully connected.

3. **Signal Processing**:
   For each valid molecule, denoise its `raw_signal` (length $N=1024$) using the Fast Fourier Transform (FFT).
   - Compute the 1D Discrete Fourier Transform of the signal.
   - Apply an ideal low-pass filter by keeping only the lowest 20 frequency components. Specifically, keep indices `0` to `19` (inclusive) and `1004` to `1023` (inclusive) unmodified. Set the coefficients for all other indices to `0`.
   - Compute the inverse FFT to get the denoised signal in the time domain. Take the real part of the result.
   - Calculate the peak amplitude ($P$) of this denoised signal (the maximum value of the array).

4. **Model Fitting & Numerical Stability Test**:
   Prepare a design matrix $X$ for Ordinary Least Squares (OLS) linear regression to predict the peak amplitude $P$ based on the Wiener Index $W$. 
   - $X$ should be an $M \times 2$ matrix, where $M$ is the number of valid molecules. The first column should be all $1$s (the intercept), and the second column should be the Wiener Indices ($W$).
   - The target vector $y$ should be the peak amplitudes ($P$).
   - Calculate the condition number of the design matrix $X$ using the 2-norm (e.g., `numpy.linalg.cond`).
   - Fit the linear model $P = \beta W + \alpha$ and find the slope $\beta$.

5. **Output**:
   Write your results to `/home/user/spectro_graphs/results.json` strictly in the following JSON format, with values rounded to 4 decimal places:
   ```json
   {
       "beta": 0.1234,
       "condition_number": 56.7890
   }
   ```