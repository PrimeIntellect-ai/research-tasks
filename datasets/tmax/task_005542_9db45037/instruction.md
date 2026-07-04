You are an integration developer setting up a local testing environment for a new API. The task involves translating a payload-signing algorithm, building a bash-based mock server, fixing a memory leak in a provided C client, and configuring its build system. 

Perform the following steps:

1. **Code Translation (Python to Bash)**
We have a legacy Python function used to calculate a simple checksum for API payloads:
```python
def compute_checksum(payload: str) -> int:
    return (sum(ord(c) for c in payload) * len(payload)) % 256
```
Translate this logic into a pure Bash script located at `/home/user/compute_checksum.sh`. 
- It must take exactly one argument (the payload string) and output ONLY the calculated integer checksum to stdout.
- Ensure the script is executable.

2. **Test Fixture / Mock Server Setup**
Create a Bash script at `/home/user/mock_server.sh` that acts as a mock API server using `nc` (netcat).
- It must listen continuously on port `8080`.
- It should accept HTTP GET requests in the format: `GET /api/verify?payload=<alphanumeric_string> HTTP/1.1`.
- It must extract the `<alphanumeric_string>` from the request path.
- It must call your `/home/user/compute_checksum.sh` script with this string.
- It must respond with a valid HTTP/1.1 200 OK response. The body of the response must be exactly: `CHECKSUM:<calculated_integer>`.
- Make sure the script is executable and loops to handle multiple sequential requests.

3. **Memory Debugging & Build System**
There is a C client located at `/home/user/api_client.c`. This client takes a payload string as an argument, constructs an HTTP GET request, connects to `localhost:8080`, and prints the server's response payload.
- **Fix the C Code:** The `api_client.c` program currently has a memory leak. Identify the missing `free()` call(s) and fix the code directly in `/home/user/api_client.c`.
- **Build System:** Write a `/home/user/Makefile` with a target named `client` that compiles `/home/user/api_client.c` into an executable named `/home/user/api_client` using `gcc`. 

4. **Verification Log**
Once you have fixed the C client and built it, use `valgrind` to verify that there are no memory leaks. Run the compiled client with the payload "hello" against your running mock server. 
Save the complete stdout and stderr output of the `valgrind --leak-check=full` run to `/home/user/valgrind_report.txt`.

Ensure all files are created exactly at the specified paths.