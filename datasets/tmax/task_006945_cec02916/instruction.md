You are a bioinformatics analyst tasked with determining whether a newly discovered DNA sequence contains a protein-coding region (exon). Coding regions often exhibit a strong "period-3" property due to the triplet nature of codons. 

Your goal is to build an automated pipeline that maps the sequence to a numerical signal, analyzes its frequency spectrum using a Fast Fourier Transform (FFT), assesses the statistical significance of the period-3 peak via bootstrapping, and analytically validates the expected noise floor.

Because your team relies on notebook-based workflow orchestration, you must implement the analysis inside a Jupyter Notebook and execute it programmatically.

Here are the step-by-step specifications:

1. **Input Data**: A DNA sequence is located at `/home/user/sequence.fasta`. (Ignore the header line starting with `>`, and concatenate the remaining lines into a single string).
2. **Signal Processing**: 
   - Map the nucleotide sequence to a numerical signal using Electron-Ion Interaction Potentials (EIIP):
     `A = 0.1260`, `C = 0.1340`, `G = 0.0806`, `T = 0.1335`.
   - Let $N$ be the length of the sequence. Compute the standard Discrete Fourier Transform (DFT) of this signal. (Use `numpy.fft.fft` without any special normalization).
   - Calculate the Power Spectral Density (PSD), defined as the absolute square of the DFT coefficients: $P[k] = |X[k]|^2$.
   - Extract the power at the period-3 frequency. The exact index for this peak is $k_{p3} = N / 3$. (You can assume $N$ is perfectly divisible by 3).
3. **Bootstrap Confidence Intervals**:
   - To check if the peak is statistically significant, establish a noise floor using a bootstrap permutation test.
   - Set the random seed: `numpy.random.seed(42)`.
   - Perform exactly 1000 iterations. In each iteration, randomly shuffle the original numerical signal, compute its FFT power spectrum, and record the power at the same index $k_{p3}$.
   - Calculate the 95th percentile of these 1000 simulated power values (use `numpy.percentile(..., 95)`).
4. **Analytical Validation**:
   - Analytically compute the expected mean power at $k_{p3}$ for a randomly permuted sequence of this composition.
   - Theoretical formula: For a randomly permuted sequence of length $N$, the expected power at any $k \neq 0$ is exactly $N \times \text{Var}(x)$, where $\text{Var}(x)$ is the population variance of the signal values (use `numpy.var` with `ddof=0`).
5. **Notebook Orchestration**:
   - Write your code in a Jupyter Notebook saved at `/home/user/period3_analysis.ipynb`.
   - The notebook, when executed, must save its final calculations to `/home/user/results.json`.
   - Create a shell script `/home/user/run_analysis.sh` that installs any required Python packages (e.g., `jupyter`, `nbconvert`, `numpy`) and executes the notebook programmatically from the command line (e.g., using `jupyter nbconvert --execute ...`).

**Output Format** (`/home/user/results.json`):
```json
{
  "sequence_length": <int>,
  "period_3_power": <float, rounded to 4 decimal places>,
  "bootstrap_95th_percentile": <float, rounded to 4 decimal places>,
  "analytical_mean_power": <float, rounded to 4 decimal places>,
  "is_coding": <boolean, true if period_3_power > bootstrap_95th_percentile>
}
```

Ensure your `run_analysis.sh` has executable permissions. You may run it to generate the output and test your pipeline.