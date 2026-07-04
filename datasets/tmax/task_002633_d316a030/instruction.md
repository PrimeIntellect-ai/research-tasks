You are a bioinformatics analyst working on a sequencing pipeline. The pipeline outputs genomic data into an HDF5 file. You need to create a pure Bash pipeline script that extracts data from the HDF5 file, performs a simple linear regression to check for GC content bias over sequence positions, and runs a regression test against a known baseline to verify pipeline consistency.

Your task is to write and execute a Bash script at `/home/user/analyze_seq.sh` that does the following:

1. **Accepts an HDF5 file path as its first argument.** (You will test it on `/home/user/data/seq_stats.h5`).
2. **Extracts Scientific Data:** Use `h5dump` (part of standard `hdf5-tools`) to extract two 1D datasets from the provided HDF5 file:
   - `/Position` (the X values)
   - `/GC_content` (the Y values)
3. **Calculates Linear Regression:** Using ONLY standard CLI tools (`awk`, `grep`, `sed`, `tr`, etc., but **no Python, R, or Perl**), calculate the slope ($m$) and y-intercept ($c$) for the linear regression equation $Y = mX + c$.
   - The slope formula is: $m = \frac{N(\sum XY) - (\sum X)(\sum Y)}{N(\sum X^2) - (\sum X)^2}$
   - The intercept formula is: $c = \frac{\sum Y - m(\sum X)}{N}$
4. **Outputs Results:** Save the computed slope and intercept to `/home/user/regression_results.txt` in exactly this format (rounded to 2 decimal places):
   ```
   Slope: [value]
   Intercept: [value]
   ```
5. **Performs Regression Testing:** The script must compare the contents of `/home/user/regression_results.txt` against a known baseline file located at `/home/user/data/baseline.txt`. 
   - If the files match exactly, write the word `PASS` to `/home/user/test_log.txt`.
   - If they differ, write the word `FAIL` to `/home/user/test_log.txt`.

**Constraints:**
- You must use Bash and standard POSIX utilities (like `awk`, `bc`, `sed`) alongside `h5dump`. Do not write Python, Perl, or R scripts to solve the math or parse the HDF5 file.
- The script must be executable.
- After writing the script, execute it against `/home/user/data/seq_stats.h5` so that `regression_results.txt` and `test_log.txt` are generated.

To complete the task, leave the executed script, `regression_results.txt`, and `test_log.txt` in their correct `/home/user/` locations.