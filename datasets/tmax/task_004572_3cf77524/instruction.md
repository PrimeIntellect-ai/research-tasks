You are acting as a bioinformatics analyst. You have been provided with two datasets from a recent proteomics experiment:
1. A FASTA file containing digested protein sequences at `/home/user/data/sequences.fasta`.
2. A CSV file containing extracted mass spectrometry peak intensities at `/home/user/data/ms_peaks.csv`.

Your objective is to build a Rust application that processes these files and performs a statistical hypothesis comparison to determine the most likely true mean of the peak intensities based on the sequence composition.

Follow these instructions to complete the task:

1. Create a new Rust binary project at `/home/user/ms_analyzer`.
2. **FASTA Parsing**: Write code to read `/home/user/data/sequences.fasta`. Calculate the total combined number of Lysine (`K`) and Arginine (`R`) residues across all sequences. Ignore header lines (lines starting with `>`). Let this count be $N$.
3. **Signal Data Parsing**: Read the peak intensities from `/home/user/data/ms_peaks.csv`. The file has a header `peak_intensity` and contains floating-point values.
4. **Hypothesis Comparison**: We assume the peak intensities are drawn from a Normal distribution with a known standard deviation $\sigma = 15.0$. We want to compare two hypotheses for the true mean $\mu$:
    *   **H0**: $\mu = N \times 5.0$
    *   **H1**: $\mu = N \times 8.0$
5. Calculate the Log-Likelihood Ratio (LLR) of H0 versus H1. 
   *Formula:* $LLR = \ln(L(Data | H0)) - \ln(L(Data | H1))$
   *(Hint: For a Normal distribution, the log-likelihood is $\sum \left[ -\frac{1}{2} \ln(2\pi\sigma^2) - \frac{(x_i - \mu)^2}{2\sigma^2} \right]$. The constant terms cancel out in the ratio).*
6. Determine the best hypothesis (`"H0"` if LLR > 0, else `"H1"`).
7. The Rust program must write the results to `/home/user/result.json` in the following exact JSON format:
```json
{
  "KR_count": <integer>,
  "LLR": <float rounded to 3 decimal places>,
  "Best_H": "<H0 or H1>"
}
```
8. Build and run your Rust program so that the `/home/user/result.json` file is generated. Ensure the output is precisely formatted.