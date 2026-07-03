I am a researcher running a molecular interaction simulation using Bash and standard Linux tools. I've encountered non-reproducible results due to floating-point reduction ordering issues when processing my network datasets. I need you to build a reliable data processing pipeline and perform a bootstrap confidence interval analysis.

You are restricted to using Bash built-ins, coreutils, `awk`, `sed`, `bc`, `shuf`, and `jq`. Do not use Python, Perl, or C++.

Here is the step-by-step task:

1. **Observational Data Reshaping & Graph Edge Calculation**
   I have a raw dataset of molecular particles at `/home/user/particles.csv`. The file has no header. The columns are `ID,X,Y,Z,Charge`.
   Write a script `/home/user/step1_pairwise.sh` that reads this file and calculates the pairwise interaction energy for all particle pairs. 
   - For every unique pair of particles $(i, j)$ where $ID_i < ID_j$:
     - Calculate the Euclidean distance $D = \sqrt{(X_i-X_j)^2 + (Y_i-Y_j)^2 + (Z_i-Z_j)^2}$.
     - If $D < 4.0$, calculate the interaction energy $E = (Charge_i \times Charge_j) / D$.
   - The script must output a file `/home/user/edges.csv` containing the pairs that meet the distance threshold.
   - Format of `edges.csv`: `ID_i,ID_j,Energy` (comma-separated, Energy rounded to 4 decimal places using standard rounding).
   - Ensure you actually run this script to generate `/home/user/edges.csv`.

2. **Fixing the Reduction Order Bug**
   There is an existing script at `/home/user/total_energy.sh` that calculates the total energy of the system by summing the energies in `edges.csv`. However, it currently reads the file in a randomized order (simulating unstable parallel reduction), and because it uses a custom truncation-based summation in `awk` to simulate low-precision hardware, the final total fluctuates depending on the order of the lines.
   Modify `/home/user/total_energy.sh` so that it first sorts the input lines deterministically (ascending by `ID_i` numerically, then by `ID_j` numerically) *before* it gets piped into the summation logic. Do not change the `awk` summation logic itself, just the pipeline order/sorting. Run this fixed script and redirect its output to `/home/user/total_fixed.txt`.

3. **Bootstrap Confidence Intervals**
   Write a script `/home/user/step3_bootstrap.sh` that performs a bootstrap analysis on the interaction energies to estimate a confidence interval.
   - It should read `/home/user/edges.csv`. Let $N$ be the number of lines (edges) in the file.
   - Perform 1000 bootstrap iterations. In each iteration:
     - Sample $N$ lines from `edges.csv` *with replacement*.
     - Sum the `Energy` column of these sampled lines (standard exact floating point addition, e.g., using `awk '{s+=$3} END {printf "%.4f\n", s}' FS=","`).
   - Collect the 1000 sums, sort them numerically.
   - Extract the 2.5th percentile (the 25th lowest value) and the 97.5th percentile (the 975th lowest value).
   - The script must output these bounds to `/home/user/ci.txt` exactly in this format:
     ```
     Lower: [Value]
     Upper: [Value]
     ```
   - Execute the script so `/home/user/ci.txt` is created.

Ensure all scripts are executable and that you leave the final requested output files (`edges.csv`, `total_fixed.txt`, `ci.txt`) in `/home/user/`.