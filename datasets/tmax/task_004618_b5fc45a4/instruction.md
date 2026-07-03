You are a performance engineer tasked with debugging and creating a regression test for a statistical profiling tool. 

The tool is located in `/home/user/app/`. There are three specific issues you need to resolve:

1. **Dependency Conflict Resolution:** 
   The tool relies on `requirements.txt`, but trying to install it via `pip install -r /home/user/app/requirements.txt` currently fails due to a dependency version conflict between `scipy` and `numpy`. Fix `requirements.txt` so that the dependencies install successfully without downgrading `scipy`.

2. **Intermittent Failure Reproduction (Bash Regression Test):**
   The tool intermittently crashes under high contention with a numerical instability issue. Create a bash script at `/home/user/app/stress_test.sh` that acts as a regression test. 
   - It must run `/home/user/app/stats_calculator.py` in parallel (e.g., 20 concurrent instances) to reproduce the high-contention environment.
   - If the script detects the string "Numerical Instability Detected" in the standard error output of *any* of the runs, `stress_test.sh` should immediately echo "Race condition reproduced" to standard output and exit with code 1.
   - If 100 total runs complete successfully without this error, it should exit with code 0.
   - Ensure the script is executable (`chmod +x`).

3. **Numerical Instability & Race Condition Diagnosis:**
   The Python script `/home/user/app/stats_calculator.py` calculates variance using shared state across a `ThreadPoolExecutor`. Because of a race condition in the `add_batch` method of `StatTracker`, the intermediate state can become corrupted, resulting in a negative variance and throwing a `math domain error` during `math.sqrt`. 
   Modify `/home/user/app/stats_calculator.py` to fix this race condition (e.g., using a thread lock) so the numerical instability is permanently eliminated.

After your work:
- `pip install -r requirements.txt` must succeed.
- Running `./stress_test.sh` *before* your Python fix should exit with 1.
- Running `./stress_test.sh` *after* your Python fix must exit with 0.