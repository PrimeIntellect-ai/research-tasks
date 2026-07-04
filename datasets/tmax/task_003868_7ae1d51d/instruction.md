You are a bioinformatics analyst tasked with filtering out synthetic DNA sequences that exhibit unnatural periodicities in their GC content. A previous researcher left a scanned note with the required methodology, but the implementation is missing.

Your objectives:
1. **Analyze the setup note:** Read the image located at `/app/lab_notes.png`. It contains the parameters for your null model, the specific metric to calculate, and the rejection threshold criteria. You can use tools like `tesseract` to read it.
2. **Monte Carlo Simulation:** Implement a Bash script (`/home/user/mc_sim.sh`) that simulates the null model described in the note. You must generate the specified number of random sequences, calculate the metric for each, and determine the exact rejection threshold. To make this efficient, use Bash parallelization (e.g., background jobs `&`, `wait`, or `xargs -P`).
3. **Data Visualization:** Create an ASCII histogram of the simulated metric values and save it to `/home/user/histogram.txt`.
4. **Create the Classifier:** Write a robust Bash script at `/home/user/detector.sh`. It must take a single file path as its argument. It should read the DNA sequence inside the file, compute the metric, and exit with status `1` (reject) if the metric is GREATER THAN OR EQUAL TO your computed threshold, and exit `0` (accept) otherwise.
5. **Output the Threshold:** Save the single integer value of your computed threshold into `/home/user/threshold.txt`.

Constraints:
- You must write your scripts entirely in Bash (using standard coreutils, `awk`, `sed`, `grep`, `$RANDOM`, etc.). Do not write Python, Perl, or C. 
- Ensure your `detector.sh` is efficient, as it will be evaluated against a massive corpus.
- The DNA sequences in the files consist only of characters `A`, `C`, `G`, `T` on a single line. Indices are 0-based.

You can test your `detector.sh` against the datasets provided in `/app/corpora/clean/` and `/app/corpora/evil/` to verify it works as expected.