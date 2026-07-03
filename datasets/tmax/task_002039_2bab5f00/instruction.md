As a data scientist, you are analyzing a periodic property embedded in a protein sequence. You need to identify the dominant frequency of this signal and analytically extract its amplitude and phase. 

Your task is to write and execute a Rust program that performs this analysis. 

Setup:
1. Create a Cargo project in `/home/user/spectral_fit`.
2. A FASTA file is located at `/home/user/sequence.fasta`. 

Your Rust program must do the following:
1. **Bioinformatics Parsing:** Parse the first sequence from `/home/user/sequence.fasta`.
2. **Signal Conversion:** Convert the sequence into a discrete numerical signal $y[n]$ by taking the ASCII decimal value of each character (e.g., 'A' = 65, 'C' = 67). 
3. **Preprocessing:** Subtract the mean of the sequence from every element to remove the DC component (create a zero-mean signal).
4. **Spectral Analysis:** Compute the 1D Forward Discrete Fourier Transform (DFT) using the `rustfft` crate. The DFT formula convention should be $X[k] = \sum_{n=0}^{N-1} y[n] e^{-i 2\pi k n / N}$.
5. **Peak Finding:** Find the frequency bin $k$ ($1 \le k < N/2$) that has the maximum magnitude.
6. **Analytical Validation:** For this dominant frequency $k$, analytically compute the peak Amplitude ($A$) and Phase ($\phi$) of the corresponding cosine wave $A \cos(2\pi k n / N + \phi)$. 
   * $A = \frac{2 |X[k]|}{N}$
   * $\phi = \text{atan2}(\text{Im}(X[k]), \text{Re}(X[k]))$

Write the extracted parameters to a JSON file at `/home/user/spectral_result.json` exactly in this format (round `A` and `phi` to two decimal places):
```json
{
  "k": 16,
  "A": 1.23,
  "phi": -0.45
}
```

Constraints:
- You must use Rust to perform the computation.
- Do not round intermediate values, only the final output values in the JSON.
- $\phi$ should be in radians in the range $[-\pi, \pi]$.