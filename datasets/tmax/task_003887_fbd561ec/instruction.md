You are an integration developer tasked with wrapping a legacy proprietary calculation engine into a modern REST API. Due to system constraints, your integration layer must be written entirely in pure Bash (using standard CLI tools like `nc`, `jq`, `awk`, etc.). 

The core calculation engine is provided as a stripped, dynamically linked binary located at `/app/bin/polycalc`. 

Your objectives are as follows:

1. **Bypass the License Check:**
   If you try to execute `/app/bin/polycalc`, it crashes or exits because of a missing shared library license check. Reverse-engineer the binary's basic requirements (e.g., using `ltrace`, `strace`, or `strings`). You will find it expects a shared object named `liblicense.so` containing a specific license verification function that returns a boolean truth (1). 
   Write a small C file, compile it into `liblicense.so` in `/home/user/`, and configure the environment so the binary successfully runs and prints its mathematical output instead of a licensing error.

2. **Implement a Bash HTTP Server:**
   Write a Bash script at `/home/user/server.sh` that implements a simple HTTP server listening on `127.0.0.1:8080`. It must run continuously.
   
3. **Parse and Transform Data:**
   The server should accept `POST` requests to the endpoint `/api/v1/math/poly`. 
   The request body will be a JSON object containing two integer parameters: `{"x": <num>, "y": <num>}`.
   Extract these integers using `jq` and pass them as command-line arguments to `/app/bin/polycalc <x> <y>`.

4. **Return Formatted Responses:**
   Capture the integer output of the binary. The Bash HTTP server must respond with a valid `HTTP/1.1 200 OK` header, followed by the correct content type, and a JSON body formatted exactly as:
   `{"status": "success", "result": <calculated_value>}`

Ensure your server is robust enough to handle multiple sequential curl requests. You may use a `while true` loop with `nc` or `socat` for the HTTP listener. 

When you have finished setting up the shared library and the server script, start your server in the background and leave it running.