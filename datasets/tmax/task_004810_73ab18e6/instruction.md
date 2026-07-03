You are a support engineer tasked with collecting diagnostics for a client's C++ physics simulation. The client complains that the final output of their simulation is losing precision, giving `3.141592741012573` instead of the expected `3.141592653589793`.

The source code for the simulation is located in `/home/user/sim`.
It compiles with the provided `Makefile`.

Your task:
1. Use debugging tools (like `gdb`) and code comprehension to locate the exact file, function, and line number where the critical precision loss occurs (where a high-precision value is inappropriately truncated or stored in a lower-precision type).
2. Create a diagnostic report at `/home/user/diagnostic.txt` with the following exact format:
```
File: <filename>
Function: <function_name>
Line: <line_number>
```
(Provide only the base filename, e.g., `simulation.cpp`, not the full path).
3. Fix the bug in the source code so that no precision is lost.
4. Recompile the project using `make` in the `/home/user/sim` directory.
5. Verify that running `/home/user/sim/sim_run` outputs exactly `3.141592653589793`.