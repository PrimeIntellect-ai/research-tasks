**Pager Alert:** 3:00 AM. 
**Incident:** The nightly data aggregation job is failing in the production pipeline. The process is crashing with a `std::domain_error` indicating a system instability.

You are the on-call engineer. The application code is located at `/home/user/app`. 

Your investigation reveals the following:
1. The start script `/home/user/app/run.sh` is crashing.
2. A recent security audit forced the removal of a hardcoded initialization token from the repository, but the pipeline requires the original production token to maintain state consistency.
3. Another recent commit supposedly "optimized" the calculation engine, but it seems to have introduced a subtle bug.

**Your Objectives:**
1. **Git Forensics & Secret Recovery:** Inspect the Git history in `/home/user/app` to find the original plaintext initialization token that was removed. Save this exact token string to `/home/user/recovered_token.txt`.
2. **Intermediate State & Precision Loss Tracking:** Analyze `/home/user/app/calc.cpp`. The program is aborting due to a precision loss issue in a hot loop that was recently modified. Identify the variable suffering from catastrophic cancellation / precision truncation and fix the data type so the assertion passes.
3. **Execution:** Recompile the fixed `calc.cpp` program (`g++ -O2 calc.cpp -o calc`). Run the compiled `./calc` binary using the recovered initialization token as its only argument.
4. **Output:** Save the final numeric standard output of the successful execution to `/home/user/output.txt`.

Ensure your fixes in `calc.cpp` strictly resolve the precision loss without altering the mathematical intent or loop bounds. Both `/home/user/recovered_token.txt` and `/home/user/output.txt` must be created with the correct values.