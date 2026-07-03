You are acting as a data scientist analyzing noisy spectroscopy data. We need to build a reproducible pipeline that smooths raw signals and fits a 2-component Gaussian mixture model to find the peak locations.

Here is your task:

1. **Compile the Signal Smoother:**
   There is a C source file located at `/home/user/src/smoother.c` which implements a simple moving average filter.
   Create a directory `/home/user/bin`.
   Compile this C file using `gcc` and place the executable at `/home/user/bin/smoother`.

2. **Process the Data:**
   You have a raw, noisy spectrum file at `/home/user/data/raw/spectrum.csv`. It contains two columns: `wavelength,intensity`.
   Create a directory `/home/user/data/processed`.
   Run your compiled `smoother` program on the raw data. The `smoother` executable takes two arguments: the window size (integer) and the input file path. It outputs the smoothed CSV to standard output.
   Use a window size of `5`.
   Save the output to `/home/user/data/processed/spectrum_smoothed.csv`.

3. **Bash Optimization Pipeline:**
   We need to find the optimal peak centers, $\mu_1$ and $\mu_2$, for the smoothed spectrum. We are assuming a fixed amplitude and variance. 
   There is a Python script at `/home/user/src/eval_mse.py` that calculates the Mean Squared Error (MSE) of a hypothetical 2-component Gaussian against the smoothed data.
   It is called like this:
   `python3 /home/user/src/eval_mse.py <path_to_smoothed_csv> <mu1> <mu2>`
   It prints a single float representing the MSE.

   Write a Bash script at `/home/user/optimize.sh` that performs a grid search to find the optimal $\mu_1$ and $\mu_2$.
   - Search space for $\mu_1$: Integers from 120 to 130 (inclusive).
   - Search space for $\mu_2$: Integers from 340 to 350 (inclusive).
   
   Your bash script must execute the search, find the pair `(mu1, mu2)` that produces the absolute minimum MSE, and write the final result to `/home/user/best_fit.txt`.
   The format of `/home/user/best_fit.txt` must be exactly:
   `mu1=[BEST_MU1],mu2=[BEST_MU2],mse=[MIN_MSE]`
   *(Note: Output the MSE exactly as printed by the python script, do not round it further).*

Ensure all created scripts are executable. Do not use external optimization libraries in Python; the grid search must be implemented strictly in Bash.