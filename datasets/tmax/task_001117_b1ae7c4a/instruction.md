You are a performance engineer tasked with profiling and debugging a set of containerized Bash mathematical optimization jobs. Recently, a specific job has been failing and causing container timeouts. 

Your objectives are as follows:

1. **Log Inspection:** Examine the application logs located in `/home/user/logs/`. Each file corresponds to a job. Identify the job that was `KILLED` due to a timeout.
2. **Query Debugging:** A SQLite database at `/home/user/jobs.db` contains the execution parameters for all jobs. The table is named `jobs` with columns `job_name`, `init_x`, and `learning_rate`. Query this database to find the `init_x` and `learning_rate` parameters used for the failing job you identified.
3. **Convergence Repair:** The optimization script is located at `/home/user/gd_optimizer.sh`. It implements a simple gradient descent to minimize a mathematical function. However, for the failing job's parameters, the optimizer oscillates and infinite loops (a convergence failure). 
   Modify `/home/user/gd_optimizer.sh` to fix this issue. Specifically, apply learning rate decay: at the very end of the `while` loop (right before `done`), multiply the current `lr` by `0.5` using `bc -l`. This will force the learning rate to decrease each iteration and guarantee convergence.
4. **Validation:** Run your repaired `/home/user/gd_optimizer.sh` using the `init_x` and `learning_rate` parameters of the failed job.

**Output Requirement:**
Take the final output value of the script (the optimized X value) for the previously failing job, round it to exactly 2 decimal places, and write it to `/home/user/solution.txt`. For example, if the output is `3.1415`, `/home/user/solution.txt` should contain exactly `3.14`.