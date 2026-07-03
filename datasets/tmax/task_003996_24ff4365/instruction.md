You are a developer debugging a mathematical simulation program located in the Git repository at `/home/user/math_sim`. 

Recently, a regression was introduced that causes the program to crash with a segmentation fault (core dump) when run with a large input. 
- The commit tagged `v1.0` is known to be good (builds cleanly and runs successfully).
- The `HEAD` commit is bad (running `./sim 10000` causes a segmentation fault).

Your task is to use `git bisect` to find the **exact single commit** that introduced this segmentation fault. 

However, there is a catch: across the 200 commits in this repository, another developer accidentally broke the `Makefile` in a large range of intermediate commits, causing a compiler/linker error (`undefined reference` to math functions due to a missing `-lm` flag). If you simply `skip` all builds that fail to compile, `git bisect` will not be able to pinpoint the exact commit (it will output a large range of possible bad commits). 

To find the precise commit that introduced the core dump, you will need to interpret the build failure and dynamically patch the `Makefile` (or manually compile with the correct flags) during your bisection testing to ensure every commit can be accurately evaluated for the runtime core dump regression.

Once you have identified the precise, single commit hash that introduced the segmentation fault, write the full, 40-character Git commit hash to `/home/user/bad_commit.txt`.

Constraints:
- Do not modify the history of the repository.
- You must find the exact single commit, not a range.