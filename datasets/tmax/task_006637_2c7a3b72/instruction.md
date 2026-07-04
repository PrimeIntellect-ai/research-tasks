You are assisting a researcher running Monte Carlo simulations to estimate integrals and analyze the convergence of the results. Your task involves setting up the scientific environment, writing a simulation script, reshaping the data, and saving it into a scientific data format.

Perform the following steps:

1. Create a Python virtual environment at `/home/user/venv`.
2. Activate the virtual environment and install the `numpy` and `h5py` packages.
3. Write a Python script at `/home/user/simulate.py` that implements a Monte Carlo integration to estimate the integral of $f(x) = e^{-x^2}$ from $x=0$ to $x=2$. The script must do the following exactly:
   - Import `numpy` and `h5py`.
   - Set the random seed using `numpy.random.seed(42)`.
   - Generate an array of 1,000,000 $x$ coordinates uniformly distributed between 0 and 2 using `numpy.random.uniform`.
   - Generate an array of 1,000,000 $y$ coordinates uniformly distributed between 0 and 1 using `numpy.random.uniform`.
   - Determine which points $(x, y)$ fall strictly under the curve (i.e., $y < e^{-x^2}$). This will give a boolean array of 1,000,000 elements.
   - Reshape this 1D boolean array into a 2D array of shape `(1000, 1000)` representing 1000 observational epochs of 1000 samples each.
   - Convert the boolean array to integers (0s and 1s) and save it to an HDF5 file at `/home/user/simulation.h5` under the dataset name `mc_epochs`.
   - Calculate the final estimate for the integral. Since the sampling bounding box has a width of 2 and a height of 1, the area of the box is 2. The integral estimate is `2.0 * (total points under curve) / 1000000`.
   - Write the final estimated integral value to a text file at `/home/user/integral_estimate.txt`, formatted to exactly 5 decimal places (e.g., `0.12345`).

4. Run the script `/home/user/simulate.py` using the Python interpreter in your virtual environment to generate the required output files.