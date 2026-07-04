You are an IT support technician. A critical ticket (Ticket #8821) has been escalated to you. The company's nightly organizational chart processor is failing, causing the HR dashboard to go down. 

The processing system is located in `/home/user/ticket_8821`. 
You can run the service using `/home/user/ticket_8821/run.sh`. 

According to the bug report, the script is experiencing multiple issues:
1. It immediately fails claiming the data file cannot be found.
2. When it does find data, it occasionally crashes with a `RecursionError`.
3. Sometimes it completes, but the final employee counts in the output are inconsistent and incorrect between runs.
4. Some incoming employee records are corrupted (missing the "department" field), which causes unhandled exceptions.

Your objective is to:
1. Fix the environment misconfiguration so the script reads from `/home/user/ticket_8821/data/`.
2. Modify `/home/user/ticket_8821/process_org.py` to gracefully skip any employee records that are missing a "department" field without crashing.
3. Fix the algorithmic bug in `process_org.py` causing infinite recursion (there are cycles in the reporting structure data that shouldn't crash the script; employees already counted in the current chain should be skipped).
4. Fix the race condition in `process_org.py` so that the multithreaded worker accurately tallies department counts.

Once you have fixed the code and environment, run `./run.sh`.
The script must successfully generate `/home/user/ticket_8821/output/summary.json` containing the correct employee counts per department.