You are a performance engineer tasked with debugging and rewriting a telemetry processing pipeline. We are migrating our aggregator from an old, unmaintained C++ binary to a new Python implementation, but the current prototype has race conditions, serialization issues, and convergence failures. 

We need you to write a clean, bug-free Python script at `/home/user/solution.py` that perfectly replicates the behavior of the old binary.

Here are your resources and constraints:
1. **The Oracle**: The original, stripped C binary is located at `/app/telemetry_oracle`. This binary takes a single line of space-separated integers on standard input (stdin) and writes a custom serialized binary payload to standard output (stdout).
2. **The Specification**: The original design document was lost, but a screenshot of the specification remains at `/app/format_spec.png`. You will need to extract the required 4-byte magic header from this image to use in your serialization format.
3. **The Calculation (Convergence & Precision)**: For each integer provided in the input, the binary calculates its square root using an iterative approximation algorithm (like the Babylonian method). However, it halts convergence at a very specific delta threshold. You must reverse engineer the `telemetry_oracle` to determine this exact stopping condition (epsilon) so your outputs match bit-for-bit.
4. **Serialization**: The output must consist of the magic header (from the image), followed by each computed value packed as a 32-bit little-endian float. 

Your goal is to write `/home/user/solution.py` such that it accepts the same text input from standard input and produces the exact same binary output on standard output as `/app/telemetry_oracle`. 

An automated fuzzer will verify your solution by feeding hundreds of random integer lists to both your script and the oracle, comparing the raw bytes of the output. 

Requirements for `/home/user/solution.py`:
- Read a string of space-separated positive integers from standard input.
- Compute the mathematically equivalent approximate square root for each number, mimicking the oracle's exact convergence threshold.
- Pack the results into the required binary format.
- Output the raw bytes to standard output.
- Ensure your script can be invoked directly as `python3 /home/user/solution.py`.