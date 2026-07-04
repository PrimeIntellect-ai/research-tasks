You are tasked with setting up a build orchestration and data verification pipeline for a small polyglot project. 

In the directory `/home/user/project`, there is a C project that generates a numerical sequence and serializes it to a JSON file. However, the project is currently broken due to a linking error in its build system. 

Your goals are:
1. **Fix the Build System**: The `Makefile` in `/home/user/project` compiles the object files but fails to link them correctly into the final executable named `app`. Diagnose and fix the `Makefile` so that running `make` successfully produces the `app` executable.

2. **Orchestrate and Verify**: Write a Bash script at `/home/user/build_and_verify.sh` that performs the following steps when executed:
   a. Navigates to `/home/user/project` and cleans any previous builds (using `make clean` if necessary, or just removing object files/binaries).
   b. Builds the C project using `make`.
   c. Executes the resulting `./app` binary. This will generate a file named `sequence.json` in `/home/user/project` containing a JSON object with a single array of integers under the key `"sequence"`.
   d. Parses the `sequence.json` file to extract the array of integers in order (you may assume `jq` is installed on the system).
   e. Implements the **Fletcher-16** checksum algorithm natively in Bash to compute a checksum over the extracted sequence of integers.
   f. Writes the final computed checksum (as a base-10 integer string) to a file at `/home/user/checksum.txt`.

**Fletcher-16 Algorithm Specification:**
- Initialize two 16-bit variables: `sum1 = 0` and `sum2 = 0`.
- Iterate through each integer `v` in the sequence. For each integer:
  - `sum1 = (sum1 + v) % 255`
  - `sum2 = (sum2 + sum1) % 255`
- The final checksum is produced by combining the two sums into a 16-bit value: `(sum2 * 256) + sum1`.

Ensure your `build_and_verify.sh` script has executable permissions. You should execute your script to ensure `/home/user/checksum.txt` is generated correctly.