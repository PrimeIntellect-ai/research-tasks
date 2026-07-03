You are a bioinformatics analyst working with UV absorption spectra to determine the concentration of different nucleotides in mixed samples.

You have been provided with two files:
1. `/home/user/pure_components.csv`: A 50x4 matrix containing the pure absorption spectra of 4 nucleotides across 50 wavelengths.
2. `/home/user/spectra.csv`: A 50x5 matrix containing the measured absorption spectra of 5 different mixed samples across the same 50 wavelengths.

Your task is to write a Python script at `/home/user/solve.py` that calculates the concentration of each nucleotide in each sample. 
To do this, you must formulate it as a linear least squares problem ($A X = B$) and solve it explicitly using **QR decomposition** (`numpy.linalg.qr`). You are not allowed to use `numpy.linalg.lstsq` or other high-level least-squares solvers.

Your script must:
1. Load the matrices from the CSV files.
2. Perform QR decomposition on the pure components matrix.
3. Solve for the 4x5 concentration matrix $X$.
4. Calculate the Residual Sum of Squares (RSS) for each of the 5 samples (i.e., the sum of squared differences between the measured spectra and the spectra reconstructed from your calculated concentrations).
5. Save the computed concentration matrix $X$ to `/home/user/concentrations.csv` (comma-separated, 6 decimal places).
6. Save the calculated RSS for each sample to `/home/user/rss.txt` (one value per line, 6 decimal places).

Run your script to generate the output files.