I'm trying to build a mathematical pipeline using a Bash script that wraps a C utility. My wrapper script, located at `/app/prime_encoder.sh`, is supposed to take a single integer `N` as an argument, retrieve the `N`th prime number by calling a local C tool, prepend the string `PRIME:`, and output the strictly base64-encoded result on a single line (no newlines, no line wrapping).

However, I'm running into multiple issues:
1. **Build Failure:** The C utility is provided as a source package in `/app/libprime-1.0.0`. When I run `make` in that directory, the build fails. There seem to be both Makefile syntax errors and linker errors (missing symbols during compilation).
2. **Boundary/Off-by-one Error:** Even if I manually compile the C utility, the wrapper script seems to return the wrong prime (for example, getting the 2nd prime when asking for the 1st).
3. **Encoding Issues:** The output from the script contains unwanted newlines and formatting errors in the base64 output, which breaks the strict single-line serialization format required by the downstream consumer.

Your tasks are:
1. Diagnose and fix the build failure in `/app/libprime-1.0.0` so that simply running `make` in that directory cleanly builds the executable `prime`.
2. Debug and repair `/app/prime_encoder.sh` so it calls the compiled `prime` binary correctly, fixes the boundary conditions, and serializes the output accurately.

Do not move or rename the wrapper script or the vendored package. A downstream automated verifier will strictly fuzz test your `/app/prime_encoder.sh` against a reference implementation with random integer inputs to ensure bit-exact equivalence.