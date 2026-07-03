You have recently inherited an unfamiliar codebase for a legacy scientific simulation tool. The tool consists of a C helper binary and a Bash wrapper script. Your predecessor left abruptly, and the system is currently broken in multiple ways. 

The codebase is located in `/home/user/sim_project/`.

Here is what you know about the system:
1. **Build Failure:** There is a build script at `/home/user/sim_project/build.sh` that compiles the helper binary. Right now, running it produces a compiler/linker error.
2. **Silent Failure:** Once built, the C binary (`/home/user/sim_project/bin/helper`) is supposed to be executed by the main script `/home/user/sim_project/simulate.sh`. However, the binary exits immediately with a failure code, and all stderr output is suppressed by the wrapper script. You will need to use system call tracing on the binary to figure out what file or resource it is failing to access, and then create that missing resource (it just needs to contain the number `100`).
3. **Precision and Convergence Loss:** After fixing the binary, `/home/user/sim_project/simulate.sh` will run its main calculation loop using `bc`. It attempts to compute the square root of the input using the Babylonian method. However, the calculation diverges or gets stuck in an infinite loop due to severe precision loss in the Bash/`bc` math step.

Your task is to:
1. Fix the build script `/home/user/sim_project/build.sh` so it successfully compiles `/home/user/sim_project/bin/helper`.
2. Trace the helper binary to find the missing input file, and create it containing the text `100`.
3. Fix the precision loss bug in `/home/user/sim_project/simulate.sh` so that the `bc` calculation properly maintains at least 10 decimal places of precision.
4. Run `/home/user/sim_project/simulate.sh`. 

When successful, `/home/user/sim_project/simulate.sh` will write the final converged result to `/home/user/sim_project/output_result.txt`. The task is complete when this file is created and contains the correct high-precision result.