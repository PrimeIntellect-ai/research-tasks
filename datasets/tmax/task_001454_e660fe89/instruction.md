You are a data analyst tasked with processing a large dataset of text sequences. We have a legacy proprietary tool located at `/app/sim_scorer` that calculates a specific similarity distance between two strings. The binary is stripped, and the original source code is lost. 

Your goal is to figure out the algorithm used by `/app/sim_scorer` by treating it as a black-box oracle (or by reverse-engineering it) and then create a highly efficient, parallelized Bash script that perfectly replicates its logic.

1. **Understand the Oracle**: 
   The tool `/app/sim_scorer` takes exactly two string arguments and prints an integer distance score. 
   Example: `/app/sim_scorer "hello" "world"`
   Analyze the outputs for various inputs to deduce how it extracts features (specifically, how it counts certain characters) and computes the distance. The inputs will only consist of ASCII letters and spaces.

2. **Implement the Replicant**:
   Write a Bash script at `/home/user/batch_scorer.sh`. 
   This script must:
   - Accept a single argument: the path to an input CSV file.
   - The CSV file will have no header and contain two columns (comma-separated strings): `string1,string2`.
   - Re-implement the distance logic of `/app/sim_scorer` purely in Bash (or standard Unix tools like `awk` / `sed` invoked from Bash).
   - Use parallel processing (e.g., `xargs -P`, `parallel`, or background jobs) to process the rows of the CSV simultaneously.
   - Output the integer scores to standard output, one per line, strictly maintaining the same order as the input CSV.

3. **Performance and Correctness**:
   Your script must not invoke the legacy `/app/sim_scorer` binary in its final implementation, as the legacy binary is too slow for our production data. Your script must be BIT-EXACT equivalent in its output to running the legacy binary on every row.

Please create `/home/user/batch_scorer.sh` and ensure it is executable. Do not leave any debugging output in the final script.