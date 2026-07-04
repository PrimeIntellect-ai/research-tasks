You are a data scientist analyzing a noisy experimental time-series dataset. The data represents sensor readings of a mechanical system that is suspected to have a stable resonant frequency. You need to identify this dominant frequency and test the convergence of your spectral analysis approach as the sample size increases.

Your task is to create a Go project that performs a Fast Fourier Transform (FFT) on the data, tests the convergence of the peak frequency estimation, and generates a visualization of the power spectrum.

**Setup Instructions:**
1. A dataset is located at `/home/user/data.csv`. It has no header. The first column is time `t` (in seconds) and the second column is the signal `y`. The data is sampled uniformly at a frequency of **200 Hz** (i.e., $\Delta t = 0.005$ s).
2. Create a Go module in the directory `/home/user/spectral` with the module name `spectral`.
3. Write your Go code in `/home/user/spectral/main.go`. You may use standard libraries and community packages such as `gonum.org/v1/gonum/dsp/fourier` for FFT and `gonum.org/v1/plot` for visualization.

**Program Requirements:**
1. **Data Loading:** Read the time-series data from `/home/user/data.csv`.
2. **Convergence Testing:** You need to determine how the estimate of the dominant frequency changes with the number of samples $N$. 
   - Loop over the following sample sizes: $N \in \{1024, 2048, 4096, 8192\}$.
   - For each $N$, take the first $N$ samples of the signal $y$.
   - Compute the FFT.
   - Calculate the magnitude of the FFT for each frequency bin (excluding the DC component, $k=0$).
   - Identify the dominant frequency (the frequency in Hz corresponding to the bin with the maximum magnitude).
   - Append the result to a log file located at `/home/user/convergence.log` using exactly the following format (rounding the frequency to 3 decimal places):
     `N=[size], PeakFreq=[freq] Hz`
     *(Example line: `N=1024, PeakFreq=12.345 Hz`)*
3. **Visualization:** For the largest sample size ($N=8192$), generate a line plot of the power spectrum (Magnitude vs. Frequency in Hz) for the positive frequencies (up to the Nyquist frequency, 100 Hz).
   - Save the plot as an SVG file to `/home/user/spectrum.svg`.

**Execution:**
Ensure your program compiles and runs successfully, producing both `/home/user/convergence.log` and `/home/user/spectrum.svg`.