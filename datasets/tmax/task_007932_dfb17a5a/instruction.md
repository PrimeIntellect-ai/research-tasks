You are a bioinformatics analyst tasked with identifying periodic genomic signals in DNA sequences using Go. Certain coding regions in DNA exhibit a strong "period-3" periodicity, which can be detected using Fourier transforms.

You have been provided with a dataset in `/home/user/data/`:
1. `reference.txt`: Contains 50 reference DNA sequences (one per line, each 1200 bases long) known to be non-coding.
2. `sample.txt`: Contains a single DNA sequence (1200 bases long) that needs to be evaluated.

Your task is to write a Go program in `/home/user/genomic_signal` that performs the following steps:

1. **Numerical Mapping**: Read the sequences and convert them into numerical signals using the following mapping:
   - 'A' = 1.0
   - 'C' = -1.0
   - 'G' = 0.5
   - 'T' = -0.5
   (Any other character should be 0.0).

2. **Spectral Analysis (FFT)**: Compute the Fast Fourier Transform (FFT) of the numerical signal for each sequence. Use the `gonum.org/v1/gonum/dsp/fourier` package. Calculate the Power Spectrum $P_k = \text{Re}(X_k)^2 + \text{Im}(X_k)^2$ for each frequency bin $k$.
   - Let $N$ be the length of the sequence (1200).
   - The corresponding frequency for bin $k$ is $f_k = k/N$.
   - Only consider the first half of the spectrum ($0 \le k \le N/2$).

3. **Numerical Integration**: For each sequence, calculate the "Period-3 Energy" ($E$) by numerically integrating the Power Spectrum $P_k$ with respect to the frequency $f_k$ over the range $0.30 \le f_k \le 0.35$ (inclusive). 
   - Use the Trapezoidal rule over the discrete points $(f_k, P_k)$ that fall exactly within this range.

4. **Statistical Comparison**: 
   - Calculate the Period-3 Energy for all 50 sequences in `reference.txt`. Find the mean ($\mu$) and the sample standard deviation ($s$) of these energies.
   - Calculate the Period-3 Energy for the sequence in `sample.txt` ($E_{sample}$).
   - Calculate the Z-score of the sample sequence: $Z = (E_{sample} - \mu) / s$.

5. **Visualization**: Use `gonum.org/v1/plot` to generate a line plot of the Power Spectrum ($P_k$ on the Y-axis vs $f_k$ on the X-axis) for the **sample sequence** (only for $0 \le k \le N/2$). Save this plot as `/home/user/output/spectrum.png`.

6. **Output**: Write your statistical results to `/home/user/output/results.json` with the following exact keys and float values:
   - `"reference_mean"`
   - `"reference_std"`
   - `"sample_energy"`
   - `"z_score"`

**Constraints & Setup:**
- You must write and execute the Go code to produce the outputs.
- Ensure all dependencies are properly initialized (`go mod init`, `go get ...`).
- Create the `/home/user/output/` directory if it does not exist.
- Do not hardcode the expected results; your program must compute them.