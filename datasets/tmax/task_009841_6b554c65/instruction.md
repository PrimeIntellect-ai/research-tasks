You are an engineer tasked with investigating a critical memory leak in a long-running mathematical Go service. The service calculates and caches the Collatz conjecture sequence for given integers.

Recently, the service has been crashing due to out-of-memory (OOM) errors. The original developer accidentally hard-deleted the source code (`server.go`) from the working directory of the repository, leaving only a compiled binary running.

Your objectives:
1. **Deleted File Recovery**: The repository is located at `/home/user/collatz-service`. The `server.go` file was committed at some point but later the commit was undone and the file was deleted. Recover the `server.go` source code from Git's dangling objects/lost-found.
2. **Packet Capture Analysis**: We have captured network traffic during one of the OOM crashes, saved at `/home/user/traffic.pcap`. Analyze this packet capture to identify the exact JSON payload (specifically, the integer value) that triggers the infinite memory allocation loop.
3. **Bug Fixing**: Identify the mathematical/logical flaw in `server.go` that causes the memory leak for the specific input found in the pcap. Fix the code so that it properly rejects invalid inputs (return an HTTP 400 status code) instead of infinitely allocating memory.
4. **Deployment**: Save the fixed code as `/home/user/fixed_server.go`. Compile and run the fixed server on port `8081`. 
5. **Reporting**: Write the precise integer value that caused the memory leak into `/home/user/poison_input.txt`.

The service expects POST requests to `/calculate` with a JSON body like `{"number": 5}`.
Ensure your fixed service runs in the background on port 8081 and properly handles the poison input without crashing or hanging.