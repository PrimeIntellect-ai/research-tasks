You are a performance engineer analyzing MCMC sampling traces. You've noticed that some simulation runs produce non-reproducible or numerically unstable results due to floating-point reduction order issues when calculating sample variance on arrays with very large means.

We use a custom library for variance and bootstrap calculations called `libstatutils`. The source for this library is vendored at `/app/libstatutils-1.2.0`. 

However, there are two issues:
1. The library is currently misconfigured. It compiles, but its numerical stability guarantees are broken due to unsafe compiler flags forced in its `Makefile` that violate strict IEEE 754 compliance and cause catastrophic cancellation to go unnoticed. You must locate the perturbation in the vendored package, fix it, and install the Python bindings via `make install_python` (which uses pip).
2. You need to create an automated filter to separate stable traces from unstable ones. 

Write a Python script at `/home/user/detect_instability.py` that takes a single file path as an argument. The script must read a CSV file containing a single column of float samples.
It should use the newly installed `libstatutils.variance(samples)` function.
If the trace suffers from catastrophic cancellation (which, after your fix, will manifest as a negative variance or exactly 0.0 for a trace that clearly fluctuates), or if the resulting variance is numerically invalid (NaN), your script must print exactly `EVIL` to standard output.
If the trace is numerically stable and produces a strictly positive variance, your script must print exactly `CLEAN` to standard output.

Your script must process the files efficiently and output only `CLEAN` or `EVIL`.