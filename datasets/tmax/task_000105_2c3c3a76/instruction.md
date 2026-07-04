You have recently joined a team and inherited a proprietary C++ mathematical compute engine located at `/home/user/project/`. The previous developer left abruptly, and the codebase is currently in an unbuildable state. Furthermore, QA reported that right before the developer left, they accidentally committed incorrect transformation constants, resulting in severe statistical anomalies in the output distribution.

Your objectives are:
1. **Fix the build failures**: The project uses a simple `Makefile`. Investigate why `make` is failing and patch the C++ source code or build configuration accordingly.
2. **Extract the correct constants**: The only remaining record of the correct mathematical constants is an image of a debugger memory dump the previous developer saved to `/app/debug_snapshot.png`. You will need to inspect this image (e.g., using `tesseract` or other vision tools) to extract the correct `multiplier` and `modulus` values.
3. **Fix the statistical anomaly**: Read the codebase in `/home/user/project/` to understand how the pseudo-random transformation is applied. Update the source code with the correct constants extracted from the image.
4. **Build the final binary**: Compile the corrected project. The final executable must be located at `/home/user/project/engine`.

The executable is expected to take a single integer argument (the initial seed), run its internal transformation loop, and print the final computed integer to standard output. An automated test suite will verify your binary by fuzzing it with random integers and comparing the bit-exact output to a secure reference oracle.

Ensure your compiled executable is named `engine` and is located in `/home/user/project/`.