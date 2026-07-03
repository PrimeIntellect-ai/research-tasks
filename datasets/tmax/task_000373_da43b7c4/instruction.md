**IT Support Ticket #8842**
**From:** Dr. Aris (Physics Dept)
**Subject:** Simulation script regression and crashes

Hello Support,

Our particle trajectory simulation script used to run perfectly, but recently it has started crashing with floating-point errors after processing large coordinates. When it crashes, it generates a custom binary state dump named `sim_memory.dmp`. 

I need you to investigate this regression in our local repository located at `/home/user/sim_repo`.

Please perform the following actions to resolve this ticket:
1. **Find the Regression:** Use Git to find the exact commit hash that introduced the crash. The initial commit was known to be good, and the current `HEAD` is bad. The script is run via `python3 simulate.py`.
2. **Analyze the Memory Dump:** When the buggy script runs and crashes, it produces a binary file `/home/user/sim_repo/sim_memory.dmp`. Extract the specific string formatted as `ERR_CODE_[A-Z_0-9]+` hidden within this dump file.
3. **Fix the Precision Bug:** The bug is caused by a catastrophic cancellation floating-point issue in the `calculate_energy(x)` function inside `simulate.py`. Specifically, evaluating `math.sqrt(x**2 + 1) - x` evaluates to exactly `0.0` for very large `x` due to floating-point precision limits, causing a division by zero later. Modify `simulate.py` in the current `HEAD` to use an algebraically equivalent formula that avoids this catastrophic cancellation (e.g., multiplying by the conjugate).
4. **Document the Findings:** Create a file named `/home/user/ticket_resolution.txt` with exactly the following format:
```
Bad Commit: <full_bad_commit_hash>
Error Code: <extracted_error_code>
```

Verify that your fixed `simulate.py` runs successfully without producing any dumps or errors.