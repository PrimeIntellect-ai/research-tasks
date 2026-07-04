I'm working as a performance engineer, and we have a custom mathematical reduction package, `calc_core`, that processes a proprietary binary sensor format. We recently received reports that our Python implementation is producing subtly different floating-point results compared to our legacy C reference binary, `legacy_calc_ref`, and is occasionally failing to parse valid edge-cases in the format.

I've placed a vendored copy of the `calc_core` package (version 1.2.3) in `/app/calc_core-1.2.3`. Unfortunately, there are a few issues you need to fix:

1. **Build Failure / Configuration:** The package currently fails to build or run its internal tests because of a misconfigured `Makefile` and missing environment variable definitions that are meant to point to the logging directory. Diagnose and fix the build.
2. **Format Parsing Edge-Case:** The parser in `calc_core/parser.py` crashes on inputs where the sensor payload length field is exactly zero. Fix it so it correctly yields an empty array instead of throwing a `struct.error` or `IndexError`.
3. **Floating-point Precision Repair:** The reduction step in `calc_core/math_ops.py` accumulates variance using a naive sum of squares approach, leading to catastrophic cancellation on inputs with large means and small variances. Refactor this to use Welford's online algorithm or a similarly stable one-pass method.
4. **Regression Test:** Write a Python script at `/home/user/regression.py` that generates a specific input file `/home/user/test.bin` which triggers the original precision bug, runs the modified `calc_core` on it, and logs the output and traceback/status to `/home/user/regression_log.txt`.

Your goal is to ensure that the command `python -m calc_core.cli <input_file>` produces BIT-EXACT identical output to `/app/bin/legacy_calc_ref <input_file>` for any valid input file.

Once you have fixed the package, please leave the corrected source code in `/app/calc_core-1.2.3`. Do not move it.