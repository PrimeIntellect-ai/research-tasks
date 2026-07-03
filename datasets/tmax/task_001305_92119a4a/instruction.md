You are a data scientist analyzing structural fluctuation signals of newly synthesized biological sequences. You have two input files:
1. `/home/user/sequences.fasta`: Contains the sequences and their IDs.
2. `/home/user/signals_raw.csv`: Contains the observational data. However, the data is poorly formatted. Each row has `seq_id, t_index, value`, but the rows are randomly shuffled. The time `t` corresponding to `t_index` is simply `t_index * 0.05`.

Your task is to write a script in a language of your choice (e.g., Python) to process this data and fit a model, then serve the results.

Here are the specific steps:
1. **Bioinformatics parsing**: Parse `/home/user/sequences.fasta` to extract the list of valid sequence IDs.
2. **Data reshaping**: Read `/home/user/signals_raw.csv` and reshape it so that for each valid sequence ID, you have an ordered time series of values sorted by `t_index`.
3. **Spectral analysis**: For each sequence's time series, use a Fast Fourier Transform (FFT) to find the dominant angular frequency $\omega_{\text{guess}}$. (Note: angular frequency $\omega = 2 \pi f$. Ignore the DC component / zero frequency).
4. **Nonlinear equation solving**: Fit the time-series data to the nonlinear model:
   $v(t) = A \sin(\omega t + \phi) + C$
   where $A > 0$ and $\phi \in [-\pi, \pi]$. Use $\omega_{\text{guess}}$ from the FFT as the initial guess for $\omega$. Use the signal's mean for the initial guess of $C$, and the signal's max minus mean for the initial guess of $A$. Set the initial guess for $\phi$ to 0.
5. **Convergence testing**: To ensure the nonlinear solver converges to the global minimum, run the solver three times for each sequence using different initial guesses for the amplitude $A$: $0.5 \times A_{\text{guess}}$, $1.0 \times A_{\text{guess}}$, and $1.5 \times A_{\text{guess}}$. Select the fitted parameters from the run that yields the lowest sum of squared residuals.
6. **Output**: Write the best-fit parameters for each sequence to `/home/user/fit_results.csv` with the exact header: `seq_id,A,omega,phi,C`. Round the numeric values to 3 decimal places.
7. **System Service**: Once the file is created, start a background Python HTTP server on port 8080 in `/home/user` so that the file is accessible at `http://localhost:8080/fit_results.csv`.

Ensure your environment has the necessary packages installed (e.g., `scipy`, `numpy`, `pandas`, `biopython` if you use Python).