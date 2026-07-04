You are an IT support technician resolving an escalation ticket. 

**Ticket details:**
"Our nightly data processing script `analyze.sh` in the repository `/home/user/reporting_tool` is failing to generate the correct totals on the `main` branch. It was last known to work perfectly at the tag `v1.0`. Additionally, the script fails to run at all in the current terminal session because of an environment misconfiguration (it throws an error about a missing configuration file)."

**Your objective:**
1. Identify and fix the environment misconfiguration so the script can execute. The required configuration file is located at `/home/user/config.ini`.
2. Use `git bisect` (and write a short bash testing script for automated bisection using assertion-based intermediate validation) to find the exact commit that introduced the calculation regression.
3. Once you identify the bad commit, save its full Git commit hash to `/home/user/bad_commit.txt`.
4. Check out the commit *immediately before* the bad commit (the last good commit) and run `analyze.sh`. Save its standard output to `/home/user/expected_output.txt`.

**Constraints & Guidelines:**
- The repository is at `/home/user/reporting_tool`.
- Do not modify the history of the repository.
- Write your output files exactly as requested so the automated verification system can validate your work.