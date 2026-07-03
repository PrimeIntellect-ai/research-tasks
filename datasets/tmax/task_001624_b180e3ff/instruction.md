You are an integration developer setting up a local CI/CD testing pipeline for a data processing component. Your goal is to write a C program that processes incoming telemetry data, configure its build system, and write a pipeline script that uses WebSockets to stream mock data to your program and verifies the output.

Perform the following tasks in the `/home/user` directory:

1. **Write the Data Processor (`/home/user/processor.c`)**
   Write a C program that reads newline-separated telemetry data from `stdin`.
   - Each line of input is a comma-separated string: `DEVICE_ID,VALUE` (e.g., `sensor_A,16.0`).
   - The program must aggregate the sum of `VALUE`s for each unique `DEVICE_ID`. (Assume a maximum of 50 unique devices and max line length of 128 bytes).
   - After processing all input (EOF), the program must calculate the square root of the accumulated sum for each device.
   - It must find the device with the highest square root value and print the result to `stdout` in exact JSON format:
     `{"top_id": "DEVICE_ID", "max_sqrt": VALUE}`
     (Format the float to exactly 2 decimal places).
   - You must use the standard C math library (`math.h`) for the square root calculation.

2. **Configure the Build System (`/home/user/Makefile`)**
   Write a Makefile to build the C program.
   - It must have a default target that builds the executable named `processor`.
   - It must link the math library dynamically using `-lm`.
   - It must include a `clean` target that removes the executable.

3. **Create the CI/CD Pipeline Script (`/home/user/ci_pipeline.sh`)**
   Write a bash script that automates the build, integration testing via WebSockets, and result verification. The script must perform the following actions sequentially:
   - Download the `websocat` binary using exactly this command:
     `wget -q https://github.com/vi/websocat/releases/download/v1.11.0/websocat.x86_64-unknown-linux-musl -O ./websocat && chmod +x ./websocat`
   - Run `make clean` and `make` to build the `processor` binary.
   - Create a file named `test_data.csv` containing exactly the following four lines:
     ```
     dev_alpha,16.0
     dev_beta,25.0
     dev_alpha,20.0
     dev_gamma,100.0
     ```
   - Start a local WebSocket server in the background on port `8080` that serves the contents of `test_data.csv` and closes the connection. Command hint: `./websocat -E ws-listen:127.0.0.1:8080 < test_data.csv &`
   - Sleep for 1 second to allow the server to bind.
   - Run a WebSocket client to connect to the server, stream the received data into your `./processor` program, and redirect the JSON output to `/home/user/result.json`. Command hint: `./websocat ws://127.0.0.1:8080 | ./processor > /home/user/result.json`
   - Parse or simply grep `/home/user/result.json` to verify if the output exactly matches: `{"top_id": "dev_gamma", "max_sqrt": 10.00}`.
   - If the output matches, write the exact string `CI PIPELINE SUCCESS` to `/home/user/ci_status.log`. If it fails, write `CI PIPELINE FAILED`.

Make sure `ci_pipeline.sh` is executable (`chmod +x`). 
Run your pipeline script at the end to ensure `/home/user/ci_status.log` is generated properly.