You are acting as a systems programmer helping to debug a C library linking issue within an end-to-end test orchestration pipeline. 

In `/home/user/project`, there is a basic pipeline that tests a Python gRPC server wrapping a C library. The bash script `/home/user/project/build_and_test.sh` is supposed to:
1. Compile `mathops.c` into a shared library (`libmathops.so`).
2. Start the Python gRPC server (`server.py`) in the background.
3. Run an end-to-end property-based test suite (`client_test.py`).
4. Clean up the background server process.

However, the pipeline is currently failing. The C library relies on the standard math library, but the compilation command in the bash script does not link it correctly, causing `server.py` to crash on startup with an `OSError: undefined symbol` error. Furthermore, the test orchestrator runs the client test immediately after spawning the server without waiting for the server to initialize its port.

Your task is to fix `/home/user/project/build_and_test.sh` using basic bash utilities so that:
1. The shared library correctly resolves math symbols dynamically (hint: link the math library).
2. The orchestrator pauses for 2 seconds before running `client_test.py` to allow the gRPC server to start.
3. If `client_test.py` finishes successfully (exit code 0), the script must write the exact string `SUCCESS` to `/home/user/project/result.log`.
4. Ensure the background Python server process is properly terminated at the end of the script regardless of test success/failure.

You only need to modify `/home/user/project/build_and_test.sh`. Do not modify the Python files or the C file. You can run `./build_and_test.sh` to verify your fix.