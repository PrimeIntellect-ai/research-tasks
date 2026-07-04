You are a support engineer tasked with collecting diagnostics for a legacy system. 

There is a local repository located at `/home/user/diagnostics_tool`. It contains a Python script `sync.py` that processes a set of timestamps and synchronizes them to UTC. 

However, there are two issues you must resolve to successfully generate the diagnostic report:

1. **Authentication missing**: The script requires an environment variable `API_SECRET` to run successfully. This secret was accidentally committed to the git repository in the past and subsequently removed. You must perform git history forensics to recover this secret.
2. **Convergence failure**: The `sync.py` script attempts to adjust a naive timestamp to match an expected UTC hour using an iterative loop. Due to a subtle bug in the timezone adjustment logic, the loop skips the target hour, fails to converge, and aborts with a convergence error.

Your task:
1. Find the `API_SECRET` in the git history.
2. Fix the convergence bug in `/home/user/diagnostics_tool/sync.py` so that the time adjustment loop correctly converges on the expected hour.
3. Run the script with the recovered secret injected as the `API_SECRET` environment variable.
4. Ensure the script successfully completes and generates the output diff report at `/home/user/diagnostic_report.txt`.

No external services need to be contacted. Only standard CLI tools and standard Python libraries are required.