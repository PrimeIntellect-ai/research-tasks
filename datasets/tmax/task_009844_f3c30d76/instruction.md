You are helping a data scientist debug a data processing pipeline. The pipeline computes the numerical integral of several time-series datasets. 

Currently, there are two major issues:
1. **Mathematical Inaccuracy:** The numerical integration is implemented using the Left Riemann Sum in `/home/user/integrate.awk`. You need to modify it to use the **Trapezoidal Rule** for higher accuracy.
2. **Reproducibility Failure:** The wrapper script `/home/user/pipeline.sh` runs the integration in parallel but writes to the output file non-deterministically. This causes our regression tests to fail because the lines in the output file are in a different order every time.

**Your objectives:**
1. Edit `/home/user/integrate.awk` to correctly implement the Trapezoidal Rule. The input files are CSVs with two columns: `time,value` (no headers). Assume the data is already sorted by time.
2. Edit `/home/user/pipeline.sh` so that the final output file `/home/user/final_output.txt` is completely reproducible. The output file must contain lines formatted exactly as `filename,integral_value` (e.g., `data_01.csv,123.456000`), and the lines **must be sorted alphabetically by filename**.
3. Run `/home/user/pipeline.sh` to generate the correct `/home/user/final_output.txt`.

Ensure the integral values in the output are printed to exactly 6 decimal places.