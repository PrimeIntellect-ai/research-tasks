You are a bioinformatics analyst tasked with calibrating a custom GC-bias scoring tool for a set of DNA sequences. The tool calculates a biological sequence score based on a parameterized model, and you need to find the optimal parameter using an optimization algorithm, validate it analytically, and calculate its confidence interval using bootstrapping.

**Setup Requirements:**
There is a C source file located at `/home/user/src/score_calc.c`. This program takes a text file of sequences and a floating-point parameter `x` as command-line arguments, and it outputs the average sequence score. The mathematical model for a single sequence's score is:
`Score = (Count_G + Count_C) * x^2 + (Count_A + Count_T) * x`

Your sequence dataset is located at `/home/user/data/sequences.txt` (one sequence per line, 100 sequences total).

**Your Tasks:**
1. **Compilation:** Create the directory `/home/user/bin` if it doesn't exist, and compile `/home/user/src/score_calc.c` into an executable named `/home/user/bin/score_calc`.

2. **Optimization:** Write a Python script to find the optimal parameter `x` (where `x > 0`) such that the average score evaluated by the `score_calc` binary for the sequences in `/home/user/data/sequences.txt` is exactly `500.0`. You must use a numerical optimization or root-finding algorithm (e.g., `scipy.optimize.minimize` or `scipy.optimize.fsolve`) wrapping the compiled C binary to find this value. 
*(Note: Analytically, the expected score follows $E[Score] = \overline{GC} \cdot x^2 + \overline{AT} \cdot x$. Use this analytical solution to validate your optimizer's result).*

3. **Bootstrap Confidence Intervals:** Modify your Python script to compute the 95% confidence interval (2.5th and 97.5th percentiles) for the optimal parameter `x` using bootstrapping.
    * Perform exactly 1000 bootstrap iterations.
    * In each iteration, sample 100 sequences from the original dataset *with replacement*. 
    * Save this resample to a temporary file, run the optimizer using the `score_calc` binary to find the optimal `x` for the resample, and record it.
    * **Crucial:** Set `numpy.random.seed(42)` immediately before your bootstrap loop to ensure deterministic resampling.

4. **Output:** Write the final results to a JSON file at `/home/user/result.json` with exactly the following structure (round the float values to 4 decimal places):
```json
{
  "optimal_x": 4.0000,
  "ci_lower": 3.9000,
  "ci_upper": 4.1000
}
```
*(Note: the values above are placeholders. You must compute the actual optimal `x`, `ci_lower`, and `ci_upper`.)*