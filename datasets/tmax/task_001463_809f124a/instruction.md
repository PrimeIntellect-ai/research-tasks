You are acting as a data scientist analyzing time-resolved spectroscopy data from a consecutive chemical reaction: $A \rightarrow B \rightarrow C$.

I have two datasets in `/home/user/`:
1. `/home/user/spectra_raw.csv`: Time-resolved absorption spectra. The first column is `time` (in seconds). The remaining columns correspond to wavelengths from 400 nm to 700 nm (e.g., `wv_400`, `wv_401`, ..., `wv_700`). This represents the mixture matrix $M$.
2. `/home/user/pure_spectra.csv`: The pure component spectra for species A, B, and C. It has a `species` column ('A', 'B', 'C') and the same wavelength columns as the raw data. This represents the spectra matrix $S$.

Your task is to unmix the spectra and determine the kinetic rate constants. Please perform the following steps:

1. **Data Reshaping and SVD**:
   Extract the time-resolved spectral matrix $M$ (ignoring the time column) and compute its Singular Value Decomposition (SVD). To confirm the underlying dimensionality of the data, extract the top 3 largest singular values. 
   Save these three values (comma-separated, in descending order, formatted to 4 decimal places) to `/home/user/svd_top3.txt`.

2. **Spectral Unmixing (Matrix Decomposition)**:
   Assuming $M \approx C S$ (where $C$ is the concentration matrix, times $\times$ 3 species), use a linear least-squares approach (e.g., QR or SVD-based `numpy.linalg.lstsq`) to estimate the concentration profiles of species A, B, and C at each time step.
   *Note: Ensure the order of columns in $C$ aligns with the species order A, B, C.*

3. **Kinetic Optimization**:
   The reaction follows a first-order consecutive mechanism:
   $A(t) = A_0 e^{-k_1 t}$
   $B(t) = A_0 \frac{k_1}{k_2 - k_1} (e^{-k_1 t} - e^{-k_2 t})$
   $C(t) = A_0 \left(1 - \frac{k_2 e^{-k_1 t} - k_1 e^{-k_2 t}}{k_2 - k_1}\right)$
   
   Using the extracted concentration profiles, fit this model to find the optimal rate constants $k_1$ and $k_2$. Use $A_0$ as the sum of the extracted concentrations of A, B, and C at $t=0$.
   Use the Nelder-Mead (simplex) algorithm (`scipy.optimize.minimize(method='Nelder-Mead')`) to minimize the total Sum of Squared Errors (SSE) across all three species and all time points. 
   Set the initial guess to $k_1 = 0.1$, $k_2 = 0.1$.
   
   Save the fitted parameters as a JSON object in `/home/user/kinetics.json` with the exact keys `"k1"` and `"k2"`. Round the values to 4 decimal places.

Do not use external libraries other than `numpy`, `scipy`, and `pandas`. Write and execute Python scripts to complete this task.