Wake up! It's 3:00 AM and you've just been paged. The nightly risk assessment pipeline, which runs critical financial calculations, has failed. The pipeline is failing consistently, and the downstream services are blocked. 

The application is a Python project located in a Git repository at `/home/user/risk_app`. The entry point that is currently failing is `/home/user/risk_app/pipeline.py`. 

Here is your incident response plan:
1. **Find the Regression:** The pipeline was working fine yesterday. Multiple commits were merged into the `main` branch today. Use Git bisection to find the exact commit that introduced the bug. 
2. **Log the Faulty Commit:** Once you have identified the first bad commit, save its full 40-character Git commit hash into a file named `/home/user/bad_commit.txt`.
3. **Diagnose and Fix the Error:** Analyze the traceback by running the pipeline. The failure is due to a numerical instability introduced during a recent code refactor. Specifically, a calculation involving logarithms is failing on zero-values in the data. Fix `pipeline.py` on the `main` branch by re-introducing a small epsilon value (`1e-9`) to the value inside the logarithm to prevent the domain error.
4. **Validate:** Verify your fix by running `python3 /home/user/risk_app/pipeline.py` and ensuring it completes successfully and prints the final score. 

You must complete all steps. The automated verification will check that `/home/user/bad_commit.txt` contains the correct hash and that the script `pipeline.py` executes without errors.