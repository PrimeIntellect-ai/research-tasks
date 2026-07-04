We are migrating our data preparation pipeline from a fragile Python environment (which kept producing "blank" matrices due to backend and library misconfigurations) to a fast, reproducible, dependency-free C implementation. 

Your task is to build this new data cleaning pipeline. You need to write a C program that performs a core linear algebra operation (matrix standardization), set up the build environment, and create bash scripts to benchmark and run the pipeline.

Perform the following steps exactly as specified:

1. **Environment Setup:**
   Create the base directory `/home/user/pipeline` and the following subdirectories inside it: `src`, `data`, `build`, and `results`.

2. **Generate the Test Dataset:**
   Create a file at `/home/user/pipeline/data/raw_matrix.csv` with exactly the following contents:
   ```
   10.0,2.0,1.0
   20.0,4.0,1.0
   30.0,6.0,1.0
   40.0,8.0,1.0
   ```

3. **C Code for Linear Algebra (Data Cleaning):**
   Write a C program at `/home/user/pipeline/src/standardize.c`. 
   - It should read a comma-separated matrix of floats from `stdin`.
   - You can assume the maximum dimensions are 100 rows and 100 columns.
   - For each column, calculate the population mean ($\mu$) and the population standard deviation ($\sigma$).
   - Standardize every element $x$ in the matrix using the formula: $z = (x - \mu) / \sigma$.
   - If a column has a standard deviation of exactly 0, the standardized value for all elements in that column should be `0.000000`.
   - Print the resulting standardized matrix to `stdout` in CSV format. Print every float to exactly 6 decimal places (`%.6f`), separated by commas.

4. **Reproducible Pipeline:**
   - Create a `Makefile` inside `/home/user/pipeline/src`. It should have a default target that compiles `standardize.c` using `gcc` with the `-O3` and `-lm` flags, and places the executable at `/home/user/pipeline/build/standardize`.
   - Write a shell script at `/home/user/pipeline/run_pipeline.sh` that:
     1. Calls `make` in the `src` directory to build the executable.
     2. Runs the executable using `/home/user/pipeline/data/raw_matrix.csv` as input.
     3. Saves the output to `/home/user/pipeline/results/cleaned_matrix.csv`.

5. **Inference Performance Benchmarking:**
   - Write a bash script at `/home/user/pipeline/benchmark.sh`.
   - This script must generate a dummy dataset of 1000 rows and 100 columns (all containing the value `1.0` separated by commas) at `/home/user/pipeline/data/large.csv`.
   - It should then measure how long it takes to execute `/home/user/pipeline/build/standardize < /home/user/pipeline/data/large.csv > /dev/null` exactly 100 times in a loop.
   - Finally, it should write the text `Benchmark completed successfully` to `/home/user/pipeline/results/benchmark.log`.

Execute all necessary commands to create these files, then run `/home/user/pipeline/run_pipeline.sh` and `/home/user/pipeline/benchmark.sh` to produce the final artifacts in the `results` directory.