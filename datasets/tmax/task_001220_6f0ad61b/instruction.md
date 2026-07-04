You are tasked with fixing a mathematical regression in our location-optimization service. The service computes the Geometric Median of a set of 2D points using Weiszfeld's algorithm. 

Recently, the service has been experiencing intermittent convergence failures (producing `NaN` or `ZeroDivisionError`), but only for specific inputs. A developer was bisecting the issue across the last 200 commits but accidentally deleted the main error log file before identifying the failing input parameters or the bad commit.

Here is your mission:

1. **Reconstruct the Failing Input**: Look in `/home/user/logs/`. The main log was deleted, but scattered log fragments across the microservices timeline (`worker_1.log`, `worker_2.log`, etc.) contain the pieces of the failing request. You need to reconstruct the list of input points and the initial guess coordinate that caused the crash.
2. **Reproduce the Convergence Failure**: Using the reconstructed parameters, reproduce the failure in the `/home/user/weiszfeld_solver` repository. 
3. **Bisect the Regression**: The repository has about 200 commits. Use `git bisect` (or write a script) to find the exact commit hash that introduced the convergence bug. 
4. **Fix the Bug**: Fix the convergence failure in the current `HEAD` of the repository. The algorithm should safely converge even if the current estimate exactly coincides with one of the input points.
5. **Generate the Output Files**:
   - Create `/home/user/bad_commit.txt` containing ONLY the full 40-character git commit hash of the commit that introduced the bug.
   - Run your fixed algorithm on the reconstructed failing input. Save the final converged `(X, Y)` coordinates to `/home/user/solution.txt` in the format `X.XXXX, Y.XXXX` (rounded to 4 decimal places).

The repository is located at `/home/user/weiszfeld_solver`. The main entry point is `solver.py`.