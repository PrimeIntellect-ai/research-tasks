You are a mobile build engineer maintaining our CI pipelines. We have a small internal telemetry tool written in C that collects build metrics, stores them in a custom hash map, and sends them to a telemetry REST API. 

However, the tool is currently broken:
1. The `Makefile` has a linking error when trying to build the project.
2. Even if you fix the build, the program crashes with a Segmentation Fault due to a memory safety issue (undefined behavior) in the custom data structure implementation (`cmap.c`).
3. The C program is supposed to serialize the map to JSON and POST it to our local python server.

Your task:
1. Navigate to `/home/user/build_telemetry`.
2. Fix the `Makefile` so that `make` successfully produces the `build_reporter` executable.
3. Fix the memory safety bug in `cmap.c`. The map stores string keys and integer values. Look closely at how strings are allocated and copied during insertion.
4. Start the local telemetry server in the background by running `python3 server.py &`.
5. Run the compiled `./build_reporter`. 

If successful, the `build_reporter` will send a POST request to the local REST API, and the server will write the received payload to `/home/user/build_telemetry/telemetry_success.json`. 

You are finished when `/home/user/build_telemetry/telemetry_success.json` exists and contains the correct JSON payload with the metrics: `apk_size`, `dex_count`, and `lint_errors`.