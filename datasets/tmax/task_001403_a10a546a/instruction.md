I am a researcher running a 1D Poisson equation simulation using Fourier spectral collocation on a periodic domain. I've been running my script on a coarse grid, but when I attempt mesh refinement to run it on a finer grid (N=256), the matrix factorization fails with a `LinAlgError: Singular matrix` error. 

This happens because the periodic Laplacian operator has a null space (constant functions), making the second-derivative matrix singular. The right-hand side of my equation integrates to zero, so a valid solution exists, but `numpy.linalg.solve` cannot handle the singularity.

Please do the following:
1. Create a Python virtual environment at `/home/user/simulation/venv`.
2. Activate it and install `numpy` and `scipy`.
3. I have placed my script at `/home/user/simulation/poisson_matrix.py`. Modify the script to fix the matrix factorization failure. You should replace the direct solver with a least-squares solver (e.g., using `numpy.linalg.lstsq`) so that it can find the minimum-norm solution despite the matrix being singular.
4. Run the fixed script with a mesh size of $N=256$.
5. The script prints the maximum value of the solution array. Save this printed numerical value directly into a new file located at `/home/user/simulation/solution_max.txt`. Do not include any other text in this file.

Ensure your environment is set up properly and that the final text file contains only the scalar float value.