You are a container specialist managing legacy microservices. We have an old, stripped binary located at `/app/data_processor` that needs to be integrated into our new automated data pipeline.

Unfortunately, this legacy binary was designed for interactive terminal use. When started, it interactively prompts the user for a service PIN and an operation mode before it begins accepting data from standard input and writing processed data to standard output. 

Your task is to write a highly optimized, robust Python script at `/home/user/run_service.py` that fully automates this execution. 

Requirements for `/home/user/run_service.py`:
1. Use Python (e.g., with the `pexpect` library or `subprocess`) to spawn `/app/data_processor`.
2. Automatically bypass the interactive prompts. You will need to analyze the binary (e.g., using `strings`, `ltrace`, or `objdump`) to discover the hardcoded service PIN. For the mode prompt ("Enable fast mode? (y/n):"), you must answer "y".
3. Once the interactive setup is complete, read the 50MB raw binary dataset from `/app/dataset.bin` and feed it into the running process's standard input.
4. Capture the processed standard output from the binary and save it to `/home/user/output.bin`.
5. **Performance Critical:** The legacy binary has a known internal buffer alignment quirk. If data is fed to it optimally, it can process the entire 50MB file in under 2 seconds. If fed sub-optimally (e.g., wrong chunk sizes or poor IPC handling), it will heavily throttle and take over 10 seconds. Your Python script must efficiently handle the IPC data transfer to complete the entire execution and data processing in **under 3.0 seconds**.

Write the Python script, ensure it has proper error handling, and verify it generates the correct `/home/user/output.bin` within the time limit.