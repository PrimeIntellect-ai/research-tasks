You are a build engineer responsible for securing our internal artifact distribution server. Currently, our artifact server is exposed to automated build agents, but it lacks strict request validation, making it vulnerable to directory traversal and unauthorized access. 

Your task is to implement a fast, lightweight HTTP request validator in C. The program will act as a pre-processor for an Nginx auth_request module, but for this task, you only need to write the standalone CLI tool.

Create a C program at `/home/user/artifact_validator.c` and compile it to `/home/user/artifact_validator`.

The program must accept exactly one argument: the absolute path to a file containing a raw HTTP request.

**Program Requirements:**
1. **State Machine Parsing:** Read the file and parse the HTTP request line and headers. You must only accept `GET` requests.
2. **URL Decoding & Routing:** Extract the URI. Implement a URL-decoder (e.g., decode `%2F` to `/`, `%2E` to `.`, etc.). After decoding:
   - The URI must begin exactly with `/artifacts/`. If it does not, output `REJECTED INVALID_ROUTE` and exit.
3. **Request Validation:** After URL decoding, check if the URI contains the directory traversal sequence `../` (or equivalent decoded forms). If it does, output `REJECTED TRAVERSAL` and exit.
4. **Token Validation:** Parse the HTTP headers to find `X-Build-Token: `. The token must be exactly 16 hexadecimal characters (0-9, a-f, A-F). If the header is missing, empty, or improperly formatted, output `REJECTED BAD_TOKEN` and exit.
5. **Success:** If all validations pass, output `VALID <decoded_uri>` (e.g., `VALID /artifacts/v1.0.1/build.tar.gz`) and exit.

**Output Format:**
The program must print exactly one line to `stdout` containing the result (`VALID ...` or `REJECTED ...`), followed by a newline `\n`. It should return exit code 0 regardless of whether the request was valid or rejected. 

Compile your code using:
`gcc -Wall -Wextra -O2 -o /home/user/artifact_validator /home/user/artifact_validator.c`

Test your program thoroughly. You can create dummy HTTP request files to ensure your URL decoding, parsing, and token validation logic works exactly as specified.