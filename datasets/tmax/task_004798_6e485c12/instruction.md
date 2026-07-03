You are an engineer investigating a critical issue in our sensor data processing pipeline. We have a C++ service that reads a stream of floating-point sensor readings, maintains a rolling window of size `K`, and outputs the rolling mean and variance. 

Recently, the service has been crashing in production due to Out-Of-Memory (OOM) errors during long runs, especially when sensor anomalies trigger window "resets". Additionally, downstream systems have flagged statistical anomalies: the variance calculations occasionally drop to zero or produce wildly incorrect spikes when sensor values are large but have low variance. 

We have a stripped, legacy binary of the correct implementation that does not leak memory and handles precision correctly. It is located at `/app/oracle_processor`.

Your workspace is at `/home/user/workspace/`. Inside, you will find:
- `processor.cpp`: The current, buggy C++ source code.
- `Makefile`: To compile `processor.cpp` into `./processor`.

The program is invoked as: `./processor <window_size>`
It reads floats from `stdin` (one per line) and writes the rolling mean and variance to `stdout` (formatted as `Mean: %.6f, Variance: %.6f`). An input of exactly `-1.0` acts as a "reset signal", which should clear the current window and start fresh.

Your tasks:
1. Identify and fix the memory leak occurring during resets. 
2. Fix the floating-point precision issue. The current naive variance calculation (`E[x^2] - E[x]^2`) suffers from catastrophic cancellation. You must implement a numerically stable method (like Welford's algorithm) to match the oracle's precision exactly.
3. Fix the boundary/off-by-one condition in the window shifting logic. The current implementation sometimes keeps `K+1` elements in the active calculation before evicting the oldest.
4. Intermediate tracing: Write your fixed code to `processor.cpp` and compile it so that the resulting `./processor` binary has identical standard output to `/app/oracle_processor` for any sequence of inputs.

The automated tests will verify your final `./processor` binary against `/app/oracle_processor` using thousands of randomly generated input streams. The output strings must match exactly. Your binary must also run cleanly under `valgrind` with no memory leaks.