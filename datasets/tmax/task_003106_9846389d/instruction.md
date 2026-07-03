You are acting as an AI assistant for a computational physics researcher. The researcher is trying to analyze high-frequency vibrational data from a simulated molecular graph network, but their data pipeline is broken and too slow.

You need to complete a multi-stage workflow to reshape the observational data, fix a vendored spectral analysis C package, parallelize it, and generate the final density estimations.

Here are the specific requirements:

1. **Observational Data Reshaping**:
   The raw output from the simulation is located at `/home/user/raw_signals.csv`. It is in a wide format where the first column is `Time`, and the subsequent columns are signal values for `Node_0`, `Node_1`, ..., `Node_999`. 
   Using standard Bash utilities (e.g., `awk`, `sed`), reshape this file into a long-format CSV saved at `/home/user/long_signals.csv` with exactly three columns: `Time,NodeID,Value`. (e.g., `0.01,0,0.453`). Ensure the header is `Time,NodeID,Value`.

2. **Fixing the Vendored Spectral Package**:
   The researcher wrote a custom C tool to perform Fourier transforms and density estimation on this data, located at `/app/libspectral-0.1`.
   - The package is failing to compute the correct spectral magnitudes. There is a mathematical bug in the magnitude calculation inside `src/spectral_density.c` (it incorrectly computes magnitude without squaring the components). You must find and fix this bug so it computes $\sqrt{re^2 + im^2}$.
   - The package is also extremely slow. The researcher attempted to use OpenMP for parallelization over the nodes, but the Makefile and the C code are improperly configured. Fix the `Makefile` to include OpenMP flags, and add the appropriate `#pragma omp parallel for` directive in `src/spectral_density.c` to parallelize the main node-processing loop.

3. **Compilation and Execution**:
   Compile the fixed package using `make` inside `/app/libspectral-0.1`.
   Run the compiled executable `./bin/analyze_spectra` on your reshaped data:
   `/app/libspectral-0.1/bin/analyze_spectra /home/user/long_signals.csv /home/user/final_densities.txt`

The final output `/home/user/final_densities.txt` must contain the correct spectral density estimations. Your final solution's correctness will be verified by calculating the Mean Squared Error (MSE) between your output and the known ground-truth density values.