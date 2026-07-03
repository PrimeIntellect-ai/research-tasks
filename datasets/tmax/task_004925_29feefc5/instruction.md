I need you to debug a failing Python port of a legacy signal processing tool. 

We are transitioning from a legacy C-based tool to a pure Python implementation. The legacy tool is provided as a compiled binary at `/app/legacy_oracle`. It reads space-separated integers from standard input, applies a proprietary filtering algorithm, and writes the transformed space-separated integers to standard output. 

A junior developer started the Python port at `/home/user/signal_port/processor.py` and wrote some tests in `/home/user/signal_port/tests/`. However, we are facing several issues:

1. **Dependency/Build Failure**: The project fails to install and run its test suite due to a dependency conflict in `/home/user/signal_port/requirements.txt`. You must diagnose and resolve this conflict so that `pytest` can run.
2. **Incorrect Output**: The Python implementation (`processor.py`) produces drastically different results than the `/app/legacy_oracle` for large input values. We suspect this is due to differences in how Python handles integer arithmetic compared to the legacy 32-bit system (which exhibited signed integer overflow wrap-around). 
3. **Missing Regression Tests**: We need a minimal reproducible example and regression test. Create a script at `/home/user/signal_port/regression.py` that generates 10,000 random integers, processes them using both the Python implementation and the `/app/legacy_oracle` binary via subprocess, and asserts that the outputs are completely identical.

**Your objectives:**
- Fix the `requirements.txt` dependency conflict.
- Comprehend the mathematical divergence in `processor.py` and fix the code to exactly replicate the `/app/legacy_oracle` behavior. The Python implementation must perfectly emulate the 32-bit signed integer overflow semantics of the original C code.
- Write the `regression.py` script.

The automated evaluation will import your `processor.py`, feed it a secret hold-out set of inputs, and measure the accuracy against the legacy oracle. You must achieve a perfect match (100% accuracy). Do not use any C-extensions; the fix must be in pure Python or using standard libraries like `numpy`.