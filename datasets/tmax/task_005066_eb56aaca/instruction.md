You are an incident responder investigating a compromised environment. We have detected that a malicious script has temporarily hijacked an authentication token and is running as a persistent background process. Additionally, the compromised system has a backend authentication authority running locally.

In the `/home/user/incident/` directory, there is a startup script named `start_scenario.sh`. This script launches two services:
1. `backend_server.py`: A local authentication authority listening on TCP port 9000.
2. `rogue_actor.py`: A malicious process that was launched with the compromised token passed insecurely as a command-line argument (specifically in the format `--stolen-auth-token=<TOKEN>`). 

Your task is to write an automated remediation service in C that will act as a local API for our security orchestration tool. 

### Instructions:
1. Run `/home/user/incident/start_scenario.sh` to initialize the environment.
2. Write a C program at `/home/user/responder.c` and compile it to `/home/user/responder`.
3. Your C program must implement a lightweight HTTP server listening on `127.0.0.1:8080`.
4. The server must handle an HTTP `GET` request to the endpoint `/remediate`.
5. When the `/remediate` endpoint is triggered, your C program must dynamically perform the following intrusion detection and response actions:
   - Iterate through the system's process hierarchy via `/proc/` to find the process executing `rogue_actor.py`.
   - Read its `cmdline` (handling null bytes appropriately) to extract the stolen token from the `--stolen-auth-token=` argument.
   - Establish a TCP connection to the backend server on `127.0.0.1:9000`.
   - Send the revocation payload exactly as: `REVOKE_TOKEN <extracted_token>\n`
   - Read the backend server's response. If successful, the backend will reply with a confirmation string containing an incident flag (e.g., `SUCCESS: FLAG_{...}`).
   - Return this exact backend response string as the body of the HTTP `200 OK` response to the `/remediate` request.
6. Start your compiled `/home/user/responder` application and leave it running in the background so that our automated verifier can query it.

Ensure your code handles basic errors (like the process not being found or TCP connection failures) and that the HTTP server stays alive to process the request from the verifier.