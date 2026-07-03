You are assisting a researcher who is running Monte Carlo numerical integrations using Bash and `awk`. The researcher has encountered a non-reproducibility bug: when calculating partial sums of a dataset in parallel and combining them, the final floating-point results slightly differ between runs. This is because background processes complete in a non-deterministic order, and floating-point addition is not strictly associative.

Your task is to fix this parallel reduction pipeline and perform a convergence test.

1. **Create the deterministic integration script**
Write a bash script at `/home/user/deterministic_integrate.sh` that takes a single filename as an argument.
The script must:
- Read the provided file (which contains one floating-point number $x$ per line).
- Split the file into smaller temporary chunk files of exactly 1000 lines each, using a consistent prefix (e.g., `chunk_`). If the file has fewer than 1000 lines, it will just be one chunk.
- Process each chunk in parallel (using bash background jobs `&`). For each chunk, use `awk` to compute the partial sum of the function $f(x) = e^{-x^2 / 2}$. The `awk` command should look like this: `awk '{s+=exp(-$1*$1/2)} END {printf "%.15f\n", s}'`.
- **Crucial Fix:** Collect these partial sums and perform the final sum. You *must* ensure that the final addition of the partial sums happens in the exact alphabetical order of the split chunk files (e.g., `chunk_aa`'s sum + `chunk_ab`'s sum, etc.), regardless of which background process finished first.
- The script must print *only* the final sum formatted to 15 decimal places. Clean up any temporary files before exiting. Make sure the script is executable.

2. **Perform a convergence test**
The researcher has provided a dataset of samples at `/home/user/samples.txt`. 
Use your script to perform a convergence test by calculating the integral estimate for the first $N$ lines of `/home/user/samples.txt`, where $N \in \{1000, 2000, 3000, 4000, 5000\}$.
Save the results to `/home/user/convergence.log`.
The log file should contain exactly 5 lines, formatted as:
`<N> <integral_estimate>`
(e.g., `1000 398.123456789012345`)

*Constraints:* 
- Use standard bash tools (`awk`, `split`, `wait`, etc.). Do not use Python, Perl, or compiled languages.