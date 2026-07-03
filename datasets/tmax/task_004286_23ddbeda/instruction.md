You are a network engineer tasked with troubleshooting and establishing a local Continuous Integration (CI) test for a custom network diagnostic tool. The tool is currently failing its connectivity checks, and its time-logging mechanism is timezone-dependent, which breaks automated log parsing.

Your objective is to back up the current state, fix the C++ code, and write a shell script that acts as a local CI pipeline to build and test the tool.

Here are your instructions:

1. **Backup Strategy**: 
   Before making any changes, create a complete tarball backup of the `/home/user/network_diag` directory. Save the archive exactly at `/home/user/archive/network_diag.tar.gz`. Ensure the `archive` directory exists.

2. **Fix the C++ Diagnostic Tool**:
   The source code is located at `/home/user/network_diag/diag.cpp`. It has two main issues:
   - It fails to compile due to missing standard network/socket headers.
   - It is supposed to connect to `127.0.0.1` on port `9999`, read a short string response from the server, and print a status line. 
   - The output must be exactly formatted as: `[YYYY-MM-DD HH:MM:SS] STATUS: <response>`
   Modify `diag.cpp` so it successfully compiles, connects to localhost port 9999, reads the incoming string, and prints the correctly formatted line using UTC time.

3. **Construct the CI/CD Pipeline Script**:
   Create a bash script at `/home/user/run_pipeline.sh`. Make sure it is executable. The script must perform the following pipeline steps:
   - Create a build directory at `/home/user/build`.
   - Compile `/home/user/network_diag/diag.cpp` into an executable named `/home/user/build/diag_tool` using `g++`.
   - Set up a simulated remote endpoint for the test: start a background process using `nc` (netcat) that listens on `127.0.0.1` port `9999` and responds with the text `ALL_CLEAR` when a connection is made.
   - Execute the compiled `diag_tool`. To guarantee the timezone configuration is strictly UTC (regardless of the system's local time), run the tool with the `TZ` environment variable set to `UTC`.
   - Redirect the standard output of the `diag_tool` run into `/home/user/pipeline.log`.
   - Ensure the background `nc` process is properly terminated or naturally exits after the connection.

Execute your pipeline script once completed to verify it works and generates the `/home/user/pipeline.log` file.