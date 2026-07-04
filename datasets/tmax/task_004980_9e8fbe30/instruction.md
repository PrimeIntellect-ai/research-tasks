You are acting as a container specialist managing a suite of microservices. We are migrating our local infrastructure and need you to configure a set of services based on an architecture diagram provided as an image.

You have been provided an image at `/app/architecture.png` that contains the text for three critical configuration parameters:
- A Web Port
- An Auth Token
- A Mock SSH Port

Your task is to implement the following using Bash and standard Linux tools (you may use Python for the HTTP server if needed, but Bash is preferred for orchestration):

1. **Extract Configuration**: Read the configuration values from `/app/architecture.png` (you can use `tesseract`).

2. **Web Service**: Start an HTTP server listening on `127.0.0.1` at the extracted Web Port. 
   - If a request is made with the HTTP header `Authorization: Bearer <Extracted_Token>`, it must respond with the exact string `M1CRO_OK` and an HTTP 200 status.
   - Any other request must receive an HTTP 401 status.

3. **Mock SSH Service**: Inspired by an SSH config that silently rejects key-based login, create a mock TCP service listening on `127.0.0.1` at the extracted Mock SSH Port.
   - When a client connects, the service must immediately send the string `SSH-2.0-RejectServer\r\n` and then gracefully close the connection.

4. **Git Repository and Hook**: 
   - Initialize a bare Git repository at `/home/user/micro_repo.git`.
   - Create a `pre-receive` hook using Bash.
   - The hook must inspect the incoming commits. If the commit message of the new commits does NOT contain the exact word `APPROVED`, the push must be rejected.
   - If it contains `APPROVED`, the push must be accepted.

5. **Orchestration**: Write a Bash script at `/home/user/start_services.sh` that starts the Web Service and the Mock SSH Service in the background and keeps them running. Ensure this script is executable. Run the script so the services are active.

Constraints:
- Do not use root privileges.
- Ensure the services are actively listening on the correct ports before finishing.