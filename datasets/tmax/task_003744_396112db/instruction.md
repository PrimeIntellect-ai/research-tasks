You are tasked with helping a researcher fix and complete a simulation analysis pipeline. The researcher is trying to perform density estimation and optimization on a simulated dataset, but their mathematical model fails due to a singular covariance matrix caused by highly correlated input features.

Your objective is to write a Python script and a bash wrapper to properly set up the environment, regularize the mathematical model, and find the optimal solution.

Specifically, you need to do the following:

1. Create a bash script at `/home/user/run.sh` that:
   - Creates a Python virtual environment at `/home/user/venv`.
   - Activates it and installs `numpy`, `scipy`, and `pandas`.
   - Executes the Python script `/home/user/analyze.py` (which you will also write).

2. Write the Python script `/home/user/analyze.py` that:
   - Loads the dataset from `/home/user/sim_data.csv`. This dataset contains two columns, `x` and `y`.
   - Computes the empirical mean vector ($\mu$) and the empirical covariance matrix ($\Sigma$) of the dataset. Because the data is highly collinear, $\Sigma$ is near-singular.
   - Regularizes the covariance matrix by adding $10^{-4}$ to its diagonal. Let's call this $\Sigma_{reg} = \Sigma + 10^{-4} I$.
   - Defines an objective function to minimize: 
     $O(x, y) = -\log( \text{pdf}(x, y) ) + \sin(x) + \cos(y)$
     where $\text{pdf}(x, y)$ is the probability density function of a bivariate normal distribution with mean $\mu$ and covariance $\Sigma_{reg}$.
   - Uses `scipy.optimize.minimize` to find the minimum of $O(x, y)$. Use the dataset's empirical mean $\mu$ as the initial guess for the optimization.
   - Saves the optimal coordinates `x` and `y` to `/home/user/solution.txt` as a single line with two comma-separated floats formatted to 6 decimal places (e.g., `0.123456,-1.654321`).

Ensure that your `run.sh` script is executable. You should run `/home/user/run.sh` to produce the final `/home/user/solution.txt` file.