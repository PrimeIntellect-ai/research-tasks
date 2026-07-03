As a bioinformatics analyst, you need to validate a legacy C tool used for calculating GC content and use it to test a biological hypothesis on a set of sequences.

Your workspace is located at `/home/user/bio_project/`. The project contains:
- `/home/user/bio_project/src/`: Contains the C source code `gc_calc.c` and a `Makefile`.
- `/home/user/bio_project/data/`: Contains 20 FASTA files (10 `case_*.fasta` and 10 `control_*.fasta`), as well as a `golden_gc.json` file.

Perform the following tasks:

1. **Compilation**: Compile the C program by running `make` in the `/home/user/bio_project/src/` directory. This will produce an executable named `gc_calc`. The executable takes a single FASTA file path as a command-line argument and prints the GC percentage as a float to standard output.

2. **Analysis Pipeline**: Write a Python script at `/home/user/bio_project/run_pipeline.py` that automates the following steps:
   
   **Phase A: Regression Testing**
   Run the compiled `gc_calc` tool on every FASTA file in the `data/` directory. Read the expected GC percentages from `/home/user/bio_project/data/golden_gc.json`. Compare the output of the tool for each file to its corresponding value in the JSON file. 
   - If the absolute difference for *any* file is greater than `0.01`, your Python script must write `Regression: FAIL` to `/home/user/bio_project/report.txt` and exit immediately.
   - If all files match within the tolerance, write `Regression: PASS` as the first line of `/home/user/bio_project/report.txt` and proceed to Phase B.

   **Phase B: Statistical Hypothesis Comparison**
   Using the GC percentages computed by the tool, separate them into two groups: `case` (from `case_*.fasta`) and `control` (from `control_*.fasta`).
   - Use `scipy.stats.ttest_ind` to perform an independent two-sample t-test comparing the case group to the control group (pass the `case` array as the first argument, and `control` as the second argument, assuming equal variance).
   - Append the results to `/home/user/bio_project/report.txt` exactly in the following format (round all floats to exactly 4 decimal places):
     ```
     Control Mean: <value>
     Case Mean: <value>
     P-value: <value>
     ```

Run your pipeline to generate the final `/home/user/bio_project/report.txt`. Ensure all dependencies (like `scipy`) are installed in your environment before running your script.