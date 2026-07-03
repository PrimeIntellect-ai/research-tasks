You are tasked with debugging a regression in a Go project located at `/home/user/math-solver`.

The repository contains roughly 200 commits. The commit tagged `v1.0` works perfectly and outputs a highly precise approximation of Pi (e.g., `3.1415826536`). However, at `HEAD`, the program's output has degraded significantly due to a precision loss issue introduced somewhere in the commit history. 

To complicate matters, another developer force-merged a series of commits into the `main` branch that temporarily broke the build (syntax errors). The build was later fixed, but the precision loss remains.

Your task:
1. Use `git bisect` to find the exact commit that introduced the algorithmic precision loss.
2. You will need to write a bisect script or manually skip the commits that fail to build, as they mask the runtime regression. A commit that fails to compile cannot be tested for precision loss and should be skipped.
3. Once you identify the first bad commit that introduced the precision degradation, write its full 40-character Git SHA to a file named `/home/user/bad_commit.txt`.

Do not modify the Git history or attempt to fix the repository. We only need the exact SHA of the commit that originally introduced the logic bug.