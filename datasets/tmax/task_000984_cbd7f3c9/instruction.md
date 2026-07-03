You are a developer tasked with fixing a broken build system and deploying a mathematical calculation service. 

We have a custom build system located in `/home/user/build_system/`. Running `./build.sh` often fails with mysterious compiler or linker errors. Even when it succeeds, the generated mathematical factor is incorrect due to precision loss in the bash calculations.

Furthermore, the deployment configuration for the resulting server has been lost from text and is only available in a screenshot located at `/app/config.png`.

Your tasks are:
1. **Extract Configuration:** Read `/app/config.png` (using OCR) to extract the target deployment `PORT` and the `AUTH_TOKEN`.
2. **Fix the Race Condition:** Analyze `/home/user/build_system/build.sh`. It runs several compilation steps in parallel, but there is a race condition causing intermittent GCC compiler and linker errors. Fix the script so it compiles reliably in parallel without conflicts.
3. **Fix the Precision Loss:** The script `/home/user/build_system/calc_factor.sh` calculates a crucial mathematical checksum factor (104348 divided by 33215), but it currently outputs a rounded integer (`3`). Modify the script using `bc` so that it calculates and outputs the value to exactly 6 decimal places (e.g., `3.141592`).
4. **Deploy the Service:** Once fixed, run `./build.sh`. It will generate a `./server.sh` script. You must run `./server.sh <PORT> <AUTH_TOKEN> <FACTOR>` using the exact values extracted and calculated.

The `./server.sh` script starts a simple HTTP server (using `socat`) that listens on the provided PORT. 
Keep this server running in the background. An automated test will verify your solution by making HTTP requests to it.