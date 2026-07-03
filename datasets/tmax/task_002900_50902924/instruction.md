You are acting as a bioinformatics analyst working with Circular Dichroism (CD) spectroscopy data to determine the secondary structure composition of a newly synthesized peptide sequence.

You have been provided with a dataset at `/home/user/cd_spectra.csv`. 
This file contains four columns:
1. `ref_alpha`: The reference spectrum for pure alpha-helix structures.
2. `ref_beta`: The reference spectrum for pure beta-sheet structures.
3. `ref_coil`: The reference spectrum for pure random coil structures.
4. `observed`: The experimentally observed spectrum for the new peptide.

Your goal is to decompose the `observed` signal into a linear combination of the three reference spectra to find the fractional composition (weights) of each secondary structure.

However, the reference spectra are highly collinear (near-singular matrix), which causes standard Ordinary Least Squares (OLS) regression to fail by producing non-physical, negative weights for some structural components.

Write a Python script to solve this problem by:
1. Loading the data from `/home/user/cd_spectra.csv`.
2. Estimating the weights of the three components (`ref_alpha`, `ref_beta`, `ref_coil`) such that the predicted spectrum best matches the `observed` spectrum, strictly enforcing that **no weight can be negative** (Non-Negative Least Squares).
3. Normalizing the resulting non-negative weights so that they sum exactly to 1.0 (representing fractional percentages).
4. Calculating the Mean Squared Error (MSE) between the `observed` spectrum and the reconstructed spectrum (using your *normalized* weights).

Output requirements:
- Save the normalized weights as a comma-separated string (in the order: alpha, beta, coil) rounded to 4 decimal places in a file named `/home/user/structural_weights.txt`.
- Save the MSE of the reconstruction rounded to 6 decimal places in a file named `/home/user/reconstruction_mse.txt`.

You may use standard Python scientific computing libraries (like `numpy`, `pandas`, `scipy`) which are already installed in the environment.