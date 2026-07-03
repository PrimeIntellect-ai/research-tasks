You are a bioinformatics analyst tasked with analyzing the hydropathy transitions of a set of protein sequences. 

You have been provided with a FASTA file containing several protein sequences at `/home/user/data/sequences.fasta`.

Your goal is to write and execute a Python script (`/home/user/analysis.py`) that performs the following steps:

1. **Parse the FASTA file:** Read the protein sequences from `/home/user/data/sequences.fasta`. Ignore any sequences that contain characters not found in the standard 20 amino acids.
2. **Hydropathy Mapping:** Convert each valid sequence into a numerical array using the Kyte-Doolittle hydropathy scale. (Use the standard values: A=1.8, R=-4.5, N=-3.5, D=-3.5, C=2.5, Q=-3.5, E=-3.5, G=-0.4, H=-3.2, I=4.5, L=3.8, K=-3.9, M=1.9, F=2.8, P=-1.6, S=-0.8, T=-0.7, W=-0.9, Y=-1.3, V=4.2).
3. **Smoothing:** For each numerical sequence, calculate a simple moving average with a window size of $W=9$. The smoothed value at index $i$ should be the average of the 9 values centered at $i$ (from $i-4$ to $i+4$ inclusive). Only calculate this for indices where the full 9-amino-acid window is available within the sequence bounds.
4. **Numerical Differentiation:** Calculate the first derivative of the smoothed hydropathy profile using the central difference method: $D_i = \frac{S_{i+1} - S_{i-1}}{2}$. Do this for all valid interior points of the smoothed sequence.
5. **Feature Extraction:** For each sequence, find the maximum absolute value of the derivative ($M$). If a sequence is too short to compute at least one derivative value, skip it.
6. **Density Estimation:** Fit a Gaussian Kernel Density Estimate (KDE) to the collection of $M$ values from all valid sequences. Use `scipy.stats.gaussian_kde` with its default bandwidth estimator.
7. **Numerical Integration:** Numerically integrate the fitted KDE from $x=1.0$ to $x=5.0$ using `scipy.integrate.quad`.
8. **Visualization:** Generate a plot of the KDE curve over the range $x=0$ to $x=5$ and save it to `/home/user/plot.png`.
9. **Output:** Write the resulting integral value (a single float, rounded to 4 decimal places) to `/home/user/results.txt`.

Ensure your script handles dependencies appropriately (you may need to install libraries like `scipy`, `numpy`, `matplotlib`, or `biopython` using `pip`).