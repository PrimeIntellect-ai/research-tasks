You are a mobile build engineer maintaining a CI pipeline for a mobile application that involves polyglot components (Python scripts orchestrating C++ Native Development Kit builds). 

Recently, the CI pipeline has been failing because the build orchestrator script (`/home/user/mobile_build/orchestrator.py`) runs out of memory and is killed by the OOM killer. The orchestrator is responsible for fetching build constraints from a local REST API, performing constraint satisfaction to determine the correct build flags, and generating a configuration file.

Your tasks are:
1. Start the local REST API server located at `/home/user/mobile_build/api.py`. It will listen on `127.0.0.1:8080`.
2. Debug and fix the memory leak in `/home/user/mobile_build/orchestrator.py`. The script implements a constraint satisfaction solver but aggressively leaks memory during exploration. You must fix it so it successfully completes without exceeding 100MB of RAM.
3. Run the fixed `/home/user/mobile_build/orchestrator.py`. It will generate a file `/home/user/mobile_build/build.env` containing the solved build flags.
4. Run `make` in `/home/user/mobile_build/` to build the C++ component using the generated `build.env` file. This will produce a binary named `libmobile.so`.
5. Write a small Python script `/home/user/mobile_build/report.py` that reads the generated `build.env` file and sends a POST request to `http://127.0.0.1:8080/report`. The JSON payload should be formatted as a dictionary of the key-value pairs from `build.env` (e.g., `{"ARCH": "...", "OPT": "...", "LTO": "..."}`).

The workspace `/home/user/mobile_build` and all necessary files have been created for you.