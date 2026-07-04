You are tasked with debugging a failing build pipeline for a data processing project located in `/home/user/project`. 

A critical configuration file, `config.b64`, was accidentally deleted and the commit that added it was wiped out via a hard reset. Fortunately, it hasn't been garbage collected by Git yet. 

Your tasks are to:
1. **Recover the deleted file**: Inspect the Git repository's dangling objects to find the missing `config.b64` file. You will know it's the right blob because its decoded content is a space-separated list of exactly 5 integers. Restore this file as `/home/user/project/config.b64`.
2. **Fix Encoding & Boundary Bugs**: The build script `/home/user/project/build.sh` is supposed to read this Base64-encoded file, decode it, and iterate over the integers to calculate a score. However, the script is failing due to incorrect decoding parameters, an off-by-one boundary error in the loop index, and an incorrectly implemented formula.
3. **Correct the Formula**: The correct formula for the score should be the sum of each `value` multiplied by `(index + 1)`, where `index` is the 0-based array index of the value. (e.g., if the array is `[10, 20]`, the score is `10*1 + 20*2 = 50`). Fix the implementation in the script.

Once you have recovered the file and fixed the bugs in `build.sh`, run the script and redirect its output (just the final calculated score as an integer) to `/home/user/project/build_output.txt`.