You are an AI assistant helping a statistical researcher with their simulation workflow.

The researcher is trying to estimate parameters for a nonlinear model using a custom Gauss-Newton optimization routine. However, their dataset contains highly collinear features (near-singular design matrix), causing the matrix factorization step in their optimizer to fail with a `numpy.linalg.LinAlgError: Singular matrix` (or similar numerical instability).

The project is located in `/home/user/sim_project/` and contains two files:
1. `optimizer.py`: Contains the custom optimization loop.
2. `simulation.ipynb`: A Jupyter Notebook that generates the synthetic data, imports the optimizer, runs the estimation, and is supposed to save the results.

Your task is to:
1. Identify and fix the numerical instability in `optimizer.py`. You must modify the code so that the matrix inversion step gracefully handles near-singular inputs (for example, by using a robust pseudo-inverse or applying a small amount of Tikhonov/Ridge regularization). 
2. Execute the Jupyter notebook `simulation.ipynb` programmatically (headless) from the terminal so that it completes successfully. 
3. The successful execution of the notebook will automatically generate a file called `/home/user/sim_project/results.csv`. Make sure this file is generated and contains the final estimated parameters as a single comma-separated line.

Do not change the random seeds or the data generation logic in the notebook, as this will change the expected statistical results.