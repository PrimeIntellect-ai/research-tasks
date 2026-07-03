You are a performance engineer tasked with replacing a legacy, unmaintainable compiled binary used for calculating performance decay metrics. The binary is located at `/app/legacy_profiler.bin`. We need a pure Python replacement that produces the EXACT same output for identical inputs, so we can integrate it directly into our Python-based testing pipeline.

Here is what you have to work with:
1. **The Legacy Repository:** There is a Git repository at `/home/user/legacy_repo`. We know that a Python prototype of the algorithm was originally committed here but was later deleted because it used incorrect baseline constants. You will need to recover this prototype to understand the base algorithm.
2. **The Specification Image:** The exact tuning constants (a `decay_rate` and a `threshold`) used to compile the final C++ binary were documented in a screenshot of a lost wiki page, now located at `/app/profiler_specs.png`. You must extract these constants from the image (e.g., using `tesseract`).
3. **The Oracle Binary:** The compiled binary `/app/legacy_profiler.bin` takes a single command-line argument consisting of a comma-separated list of execution times (integers) and prints a final calculated float score to standard output. 

Your task is to create a Python script at `/home/user/profiler_calc.py` that takes a single command-line argument (a string of comma-separated integers) and prints the exact same output as `/app/legacy_profiler.bin`. 

Your script will be tested automatically by fuzzing it with hundreds of random integer sequences to ensure 100% equivalence with the oracle binary. Do not wrap the output in any extra text; just print the final number identically to the binary.