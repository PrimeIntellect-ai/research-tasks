I am a researcher running observational simulations for a new radio telescope, and I need help processing a large dataset of simulated spectra. The data is currently in a raw binary format and needs to be processed efficiently using parallel computing.

I have a file at `/home/user/spectra.dat` which contains 1000 signals. Each signal consists of 2048 `double` precision floating-point numbers (8 bytes each). The data is stored sequentially (Signal 0, Signal 1, ..., Signal 999).

Please write a C program named `/home/user/process_spectra.c` that does the following:
1. Reads the `/home/user/spectra.dat` file.
2. Uses OpenMP to process the signals in parallel.
3. For each signal $j \in [0, 999]$, applies a Hanning window to the samples $x[i]$ for $i \in [0, 2047]$. The Hanning window equation is:
   $w[i] = 0.5 \times \left(1.0 - \cos\left(\frac{2 \pi i}{M - 1}\right)\right)$
   where $M = 2048$.
   The windowed signal is $x_{w}[i] = x[i] \times w[i]$.
4. Computes the total energy of each windowed signal, which is the sum of the squared windowed samples:
   $E_j = \sum_{i=0}^{2047} (x_{w}[i])^2$
5. Writes the results to `/home/user/energies.csv`. The CSV should have a header `Signal_ID,Energy` and 1000 lines of data formatted as `%d,%.6f`.

After writing the C program, compile it into an executable named `/home/user/process_spectra` with OpenMP enabled (use `gcc` and `-lm` for the math library). Then, run the executable.

Finally, write a Python script `/home/user/plot_energies.py` that reads `/home/user/energies.csv` and creates a scatter plot of Energy vs. Signal_ID. Save the plot as `/home/user/energies_plot.png`. Run this Python script to generate the image.

Ensure that:
- The C code strictly uses OpenMP for parallelizing the loop over the signals.
- The output CSV is exactly in the specified format.
- The Python script uses `matplotlib` (which is already installed in the environment).