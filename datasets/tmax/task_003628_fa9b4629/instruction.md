You are an integration developer tasked with building a lightweight API service that evaluates a sequence of mathematical operations embedded in an audio file.

You have been provided with an audio artifact located at `/app/fixture.wav`. This file contains hidden operational commands encoded in a custom metadata chunk. 

To extract these commands, your team has provided a C-based extractor tool located in `/app/extractor/`. However, the tool is currently broken due to a build configuration issue.

Your task is to complete the following workflow using standard Bash tools, coreutils, and the provided files:

1. **Fix the Build**:
   Navigate to `/app/extractor/`. The `Makefile` has a linking error preventing the compilation of the `extractor` binary. Identify the issue (hint: it relates to a missing standard library flag for mathematical functions) and fix the `Makefile`. Run `make` to successfully build the `./extractor` executable.

2. **Extract Data**:
   Use the compiled `./extractor` to parse the audio file:
   `./extractor /app/fixture.wav > /home/user/commands.txt`
   The extracted file will contain a sequence of instructions, one per line (e.g., `LOAD <num>`, `ADD <num>`, `SUB <num>`, `MUL <num>`, `DIV <num>`).

3. **Implement a Bash Interpreter**:
   Write a pure Bash script at `/home/user/interpreter.sh` that reads `/home/user/commands.txt`, parses the structured commands, and evaluates them sequentially against a single integer accumulator. The accumulator should default to `0` unless a `LOAD` command sets it. The script should output ONLY the final integer result to stdout.

4. **Deploy a Multi-Protocol Service**:
   Write a Bash script at `/home/user/server.sh` that acts as a simple HTTP server using `nc` (netcat) or `socat`. 
   - The server must listen on `127.0.0.1:9090`.
   - When the server receives an `HTTP GET /state` request, it should execute `/home/user/interpreter.sh` to dynamically compute the result.
   - It must respond with a valid `HTTP/1.1 200 OK` header, `Content-Type: application/json`, and a JSON body formatted exactly as: `{"accumulator": <final_value>}`.
   
5. **Start the Service**:
   Run `/home/user/server.sh` in the background so that it is continuously listening on port 9090. Ensure it can handle multiple sequential requests without crashing.

Complete all steps ensuring the server is active and bound to the correct port at the end of your session.