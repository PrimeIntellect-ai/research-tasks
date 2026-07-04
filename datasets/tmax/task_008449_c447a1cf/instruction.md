You are tasked with debugging a critical mathematical optimization tool written in Go that has recently stopped working. 

The repository is located at `/home/user/opt-repo`. The tool uses the Newton-Raphson method to find the roots of a complex polynomial. However, developers have reported two major issues:
1. The tool currently fails to run on the `main` branch because a required input configuration file was accidentally deleted in a recent commit.
2. Even if you provide the configuration, the algorithm suffers from a convergence failure (it reaches the maximum iterations without finding a root, producing an error). This is a regression that was introduced somewhere in the last 200 commits.

Your objectives are:
1. **Recover the input file**: Inspect the git history to find and restore the accidentally deleted `params.json` file to the root of the repository.
2. **Bisect the regression**: Use `git bisect` (or a similar technique) across the repository's history (between `HEAD` and `HEAD~200`) to find the exact commit that introduced the convergence failure. 
3. **Report the bad commit**: Once you find the commit hash that introduced the math bug, write its full 40-character SHA-1 hash to `/home/user/bad_commit.txt`.
4. **Repair the convergence failure**: Analyze the mathematical logic in the bad commit, figure out what went wrong with the derivative calculation or update rule, and fix the bug in `main.go` on the current `main` branch.
5. **Compute the final result**: Run the fixed `main.go` with the recovered `params.json`. The program will output a single floating-point number representing the root. Save this exact numeric output to `/home/user/solution.txt`.

Constraints:
- Do not modify the commit history (e.g., do not rebase or commit your fix). Just leave the modified `main.go` in the working directory on the `main` branch.
- The `params.json` file must be exactly as it was before deletion.