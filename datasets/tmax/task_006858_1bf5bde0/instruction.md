You are a debugging expert tasked with resolving a regression in a C project. 

A repository located at `/home/user/sorter_repo` contains a custom sorting implementation (`sort.c`, `main.c`, `Makefile`, and a test script `test.sh`). 

Recently, developers noticed that the program sometimes crashes with a segmentation fault or hangs indefinitely. This regression was introduced somewhere within the last 200 commits. 

Your objectives are:
1. Identify the exact commit that introduced the bug. The bug involves an off-by-one error in a boundary condition that causes infinite recursion.
2. Fix the bug in the latest version (`HEAD`) of `sort.c`.
3. Write the full 40-character commit hash of the first bad commit to `/home/user/bad_commit.txt`.
4. Save your corrected version of `sort.c` to `/home/user/fixed_sort.c`. 

The `test.sh` script in the repository is guaranteed to exit with code `0` on a good commit and a non-zero code on a bad commit. You may use any tools or scripts (such as `git bisect`) to find the regression. Do not push or commit any changes to the repository; just provide the requested files in `/home/user`.