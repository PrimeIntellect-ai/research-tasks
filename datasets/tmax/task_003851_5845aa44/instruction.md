We are building a Monte Carlo simulation and statistical fitting tool that processes molecular coordinate data in the PDB format. Unfortunately, our previous parallel implementation produces non-reproducible results across different runs due to floating-point reduction order variations. 

We need a bit-exact, deterministic C++ implementation that parses PDB coordinates and uses Kahan summation to guarantee numerical stability and determinism, matching our strict reference oracle.

Your task:
1. Examine the image located at `/app/parameter.png`. It contains a handwritten note with a scalar simulation parameter. Extract this numerical value.
2. Write a C++ program at `/home/user/compute_stat.cpp` and compile it to an executable at `/home/user/compute_stat`.
3. Your program must read a stream of text lines from standard input (`std::cin`).
4. For each line that begins exactly with the string `ATOM  `, extract the X coordinate. According to the standard PDB format, the X coordinate is located at columns 31-38 (1-based index, which corresponds to string indices 30 to 37).
5. Parse this X coordinate as a standard double-precision float (`double`). Ignore lines that do not start with `ATOM  ` or do not have enough characters. If the extracted string cannot be parsed as a valid double, consider its value to be `0.0`.
6. Multiply each parsed X coordinate by the scalar parameter you extracted from the image.
7. Accumulate these values using the standard Kahan summation algorithm to ensure deterministic floating-point precision.
8. Output ONLY the final sum on a single line, formatted to exactly 8 decimal places (e.g., `0.00000000`). If no valid `ATOM  ` lines are processed, output `0.00000000`.

Our automated test suite will run a fuzzing verification against your `/home/user/compute_stat` binary. It will generate thousands of random and well-formed inputs and assert that your binary's output perfectly matches our hidden reference oracle bit-for-bit.