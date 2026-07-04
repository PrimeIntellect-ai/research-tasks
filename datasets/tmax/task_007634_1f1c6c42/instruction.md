You are an IT support technician acting as a Level 3 escalation engineer. We received an urgent ticket (Ticket #8832) from the quantitative analysis team. They have a distributed C++ microservice that calculates convergence points for financial models. 

Recently, the system has been producing incorrect query results and intermittently failing to converge for certain input streams. The users suspect a hardware architecture issue, but our initial triage points to a software bug involving precision loss and integer overflow under specific conditions.

Your objective is to debug and resolve this ticket by completing the following steps:

1. **Log Timeline Reconstruction:**
   The service runs on three nodes. The logs from the last run are located in `/home/user/ticket_8832/logs/`. They contain mixed timestamps.
   Write a script to aggregate, parse, and chronologically sort all log entries from these three files. 
   Save the chronologically sorted log to `/home/user/ticket_8832/timeline.log`.
   Identify the specific `job_id` and `input_value` that caused the convergence failure (it will be evident in the logs as an unexpected termination or error).

2. **Convergence Failure Repair & Precision Debugging:**
   The source code for the calculation engine is at `/home/user/ticket_8832/src/optimizer.cpp`.
   Analyze the C++ code. You will find that the convergence algorithm intermittently fails or returns incorrect values due to a combination of signed integer overflow and floating-point precision loss.
   Modify `optimizer.cpp` to fix these bugs. The variables should have sufficient precision (e.g., `double` instead of `float`) and the iteration counters must not overflow before reaching the maximum allowed iterations (40000).

3. **Recompilation and Intermittent Failure Reproduction:**
   Recompile the fixed program. A Makefile is provided in `/home/user/ticket_8832/src/`. Simply run `make` in that directory to produce the `optimizer_service` executable.
   Run the fixed executable using the problematic `input_value` you identified from the logs:
   `./optimizer_service <problematic_input_value>`
   This will run the convergence engine and automatically update the local SQLite database.

4. **Query Result Debugging:**
   The results are stored in a SQLite database at `/home/user/ticket_8832/db/results.db` in the table `convergence_runs`.
   Before your fix, the failed run inserted a corrupted/failed record for the problematic `job_id`. Your successful run just inserted a new record for the same input but with a new timestamp.
   Extract the corrected final convergence `result_value` for this specific input from the database.
   Save *only* the numeric result (rounded to 4 decimal places) to `/home/user/ticket_8832/final_answer.txt`.

Ensure all requested output files (`timeline.log` and `final_answer.txt`) are created exactly at the specified paths.