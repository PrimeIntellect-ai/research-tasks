You are a support engineer investigating a critical failure in a C++ scientific simulation engine. The application crashed in production, leaving behind a core dump.

The environment contains the following files:
- Executable: `/home/user/sim_engine`
- Core dump: `/home/user/core`
- Source code directory: `/home/user/src/` (contains `sim_engine.cpp`)

Your objectives are to perform forensic analysis on the core dump, fix the underlying precision-related bug, and verify the fix.

Please complete the following steps:
1. **Core Dump Analysis:** Use `gdb` to analyze `/home/user/core` and `/home/user/sim_engine`. The application crashed while processing a specific session. Extract the 32-character `session_id` string from the memory of the crashed frame.
2. **Precision Loss Tracking:** Inspect the stack trace and codebase to find the root cause. A precision loss occurs due to an incorrect type signature in a math function, which eventually truncates a very small number to `0.0`, resulting in a divide-by-zero Floating Point Exception (SIGFPE).
3. **Code Fix:** Modify `/home/user/src/sim_engine.cpp` to fix the precision loss. Ensure that the mathematical calculation maintains double precision and does not truncate the time delta.
4. **Recompilation:** Recompile the fixed application to a new executable at `/home/user/sim_engine_fixed`. Use the command: `g++ -g -O0 /home/user/src/sim_engine.cpp -o /home/user/sim_engine_fixed`
5. **Reporting:** Create a diagnostic report at `/home/user/report.txt` with exactly the following format:
```
SESSION_ID:<extracted_session_id>
CRASH_FUNCTION:<name_of_the_function_where_the_crash_occurred>
FIXED_PARAM:<name_of_the_parameter_whose_type_you_changed>
```

Example of `report.txt`:
```
SESSION_ID:TXN-0000-MOCK-ID
CRASH_FUNCTION:compute_trajectory
FIXED_PARAM:time_step
```

Ensure your repaired executable `/home/user/sim_engine_fixed` runs successfully without crashing.