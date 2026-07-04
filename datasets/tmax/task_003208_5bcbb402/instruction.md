You are a data scientist working on a Bash-only reproducible pipeline to model binding affinities of specific DNA primer regions. 

You have been provided a dataset of DNA sequences in `/home/user/dna_sequences.txt`.

Your task is to write a Bash shell script at `/home/user/pipeline.sh` that does the following:

1. **Primer Sequence Alignment:** 
   Extract all DNA subsequences from `/home/user/dna_sequences.txt` that match the following primer pattern: starts with `GATA`, ends with `CACA`, and has exactly 5 to 10 characters (inclusive) of any standard DNA base (A, T, C, G) in between. 
   *(Extract only the matching portions, each on a new line, in the order they appear).*

2. **Monte Carlo Numerical Integration:**
   For each extracted primer sequence, calculate its length, $L$. We want to estimate the "binding energy", defined as the integral of $f(x) = \frac{x^2}{L}$ from $x = 0$ to $x = L$.
   
   To do this, implement a Monte Carlo integration algorithm strictly using `awk`. Since standard `awk` `rand()` implementations can vary between GNU/BSD versions, you must build a custom Linear Congruential Generator (LCG) for reproducibility.
   
   **LCG Specifications:**
   - Initial Seed: `123` (Initialize this once at the very beginning of the awk execution, not per sequence).
   - LCG Formula: `seed = (1103515245 * seed + 12345) % 2147483648`
   - Random Float in [0, 1): `r = seed / 2147483648`
   - To sample $x$ in $[0, L]$, use: `x = r * L`

   For each extracted sequence:
   - Run $N = 1000$ iterations.
   - In each iteration, generate $x$ using the LCG, compute $y = \frac{x^2}{L}$, and keep a running sum of $y$.
   - Calculate the sequence's integral estimate: $\text{Integral} = \left(\frac{\text{sum of } y}{1000}\right) \times L$.

3. **Output:**
   Sum the integral estimates of all matching primer sequences. Save ONLY this final sum, rounded to exactly two decimal places (e.g., `235.42`), to `/home/user/total_energy.txt`.

Ensure your `/home/user/pipeline.sh` script is executable (`chmod +x`) and runs without errors.