**IT Support Ticket #8921: Legacy Sensor Calculation Tool Recovery**

**Status:** Open
**Priority:** High
**Assignee:** Data Processing Support Technician

**Issue Description:**
We've had a critical failure on our edge sensor node. A power loss corrupted the main file system, destroying the source code for our primary sensor metric calculator. We managed to recover an old, buggy version of the source code (`/home/user/sensor_calc_old.c`) and a stripped binary of the *latest, fixed* version (`/app/sensor_calc_oracle`). 

The old source code suffers from severe numerical instability. When processing sensor readings that have a large base value but small fluctuations, it intermittently produces wildly incorrect results, `NaN`, or crashes due to floating-point exceptions (catastrophic cancellation). The oracle binary (`/app/sensor_calc_oracle`) does not have this bug; it implements a numerically stable formula to calculate the exact same requested metrics (Count, Mean, and Sample Variance).

To help you reproduce the intermittent failures and test your assumptions, I've also attached a recovered, partially corrupted SQLite WAL file (`/app/db/metrics.db-wal`) containing some historical sensor data strings before the crash.

**Your Objective:**
1. Analyze `/home/user/sensor_calc_old.c` to understand the inputs and the intended output format.
2. Observe how the black-box binary `/app/sensor_calc_oracle` behaves differently from the old code, especially on inputs with large magnitudes and small variances.
3. Diagnose the numerical instability in the old formula and deduce the stable algorithm the oracle is using.
4. Write a corrected C program at `/home/user/sensor_calc.c`.
5. Compile it to `/home/user/sensor_calc`.

Your compiled executable (`/home/user/sensor_calc`) must be **bit-for-bit identical** in its standard output and exit codes to `/app/sensor_calc_oracle` for *any* valid sequence of floating-point numbers provided as command-line arguments. 

**Execution:**
The program takes floating-point numbers as command-line arguments:
`./sensor_calc 1000000.1 1000000.2 1000000.3`

Do not add extra debug output to the final compiled binary. It must be a silent, drop-in replacement that strictly matches the oracle's output.