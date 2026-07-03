You are tasked with fixing a broken polyglot project (Python + C) located in `/home/user/workspace/pynode_proc`.

The package is intended to be a high-performance data processor, but the previous developer left it in a broken state:
1. **Broken Build:** The `setup.py` is misconfigured and fails to properly compile and link the C extension `_fastnode.so`. 
2. **Missing C API integration:** The C struct definitions and function exports are incomplete. You need to recover the exact struct layout and target function name from a design diagram located at `/app/struct_spec.png`.
3. **Memory Safety Bugs:** Once it builds, running the property-based tests (`python -m pytest test_prop.py`) causes a Segmentation Fault due to undefined behavior (memory corruption/buffer overflow) in `fastnode.c`.
4. **Performance Target:** After fixing the memory bugs, you must run `python benchmark.py`. It evaluates the C extension against a pure-Python fallback.

**Instructions:**
1. Extract the required struct fields and function signature from `/app/struct_spec.png`.
2. Update `fastnode.c` to match this specification and fix the memory corruption bug (ensure no out-of-bounds writes or memory leaks).
3. Fix `setup.py` so that `pip install -e .` successfully builds the C extension.
4. Verify your fixes by running `pytest test_prop.py`. It uses the `hypothesis` library to fuzz the C API and should pass 100% of the cases without segfaulting.
5. Run `python benchmark.py` which outputs a single execution time value (in seconds) to the console.
6. Write this exact floating-point number into `/home/user/workspace/pynode_proc/metric.txt`.

Your goal is to achieve an execution time of **less than 0.5 seconds** on the benchmark.