You have inherited an unfamiliar codebase located at `/home/user/project`. This project contains a data processing pipeline that calculates the sum of square roots of numbers provided in text files, using a custom multithreaded iterative solver (Newton's method). 

Currently, the pipeline is completely broken:
1. The wrapper script `run_pipeline.sh` fails to process files in the `data/` directory because it breaks on filenames containing spaces.
2. The core C program `solver.c` used to work perfectly, but a recent commit introduced a race condition that causes a **convergence failure** (threads hit the maximum iteration limit and output "Failed to converge").

Your objectives are:
1. **Fix the shell script:** Modify `run_pipeline.sh` so it correctly iterates over and processes all files in the `data/` directory, even those with spaces in their names.
2. **Identify the regression:** Use `git bisect` (or manual git log inspection) to find the exact commit hash that introduced the convergence failure in the C code. Write this full commit hash to a new file at `/home/user/bad_commit.txt`.
3. **Debug and repair the C code:** Use an interactive debugger or code inspection to find the race condition in `solver.c`. Fix the bug so that the algorithm converges correctly for all data points.
4. **Run the pipeline:** Recompile the `solver` (using `gcc -O2 -pthread solver.c -o solver -lm`) and run your fixed `./run_pipeline.sh`. Redirect the standard output of the pipeline to `/home/user/pipeline_output.txt`.

Constraints & Requirements:
- The fixed `solver.c` must remain multithreaded and maintain the same thread structure (do not revert the file to the single-threaded version).
- Do not modify the data files.
- Ensure the final output in `/home/user/pipeline_output.txt` contains the successful output format: `File: <filename> | Sum of roots: <value>` for each file.