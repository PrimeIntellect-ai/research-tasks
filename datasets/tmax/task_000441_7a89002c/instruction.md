I'm trying to build and run an optimization tool for a project, but the build is failing and the optimization process keeps diverging. 

Here is the setup:
1. I have a vendored third-party library `liblbfgs-1.10` located at `/app/liblbfgs-1.10`. It currently fails to compile because of a deliberate issue introduced during a bad merge (a missing `#include` and a typo in the `Makefile.am` / `Makefile.in` or similar build script, causing a dependency conflict/build failure). Please fix the vendored package and install it locally to `/app/local`.
2. My main project is in `/app/project`. It links against `liblbfgs` to minimize a cost function based on sensor data.
3. The sensor data in `/app/project/sensor_data.csv` is slightly corrupted. Some of the float values are `NaN` or `inf`. You must modify `/app/project/main.c` to detect and replace these invalid values with `0.0` before passing them to the optimizer.
4. The objective function in `/app/project/main.c` is currently failing to converge. There is a bug in the gradient calculation inside the `evaluate()` function (it has the wrong sign or missing a term for the Rosenbrock-like function being fitted). 
5. Fix the build script in `/app/project/Makefile` to properly link against `/app/local/lib/liblbfgs.a` and include `/app/local/include`.

Your goal:
1. Successfully build `/app/project/optimize_sensor`.
2. Run `/app/project/optimize_sensor`. It should output the final minimized cost to `/app/project/result.txt` in the format `Final cost: <value>`.
3. The optimization must successfully converge, and the final cost must be properly minimized. 

Please go ahead and diagnose the build errors, handle the corrupted inputs in the C code, fix the convergence failure by correcting the math in the gradient, and produce the final result file.