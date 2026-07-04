You are a Linux systems engineer. We are experiencing an outage in our local staging environment because our proxy cannot connect to our custom C-based backend daemon. The proxy expects the backend to be listening on a UNIX domain socket at `/home/user/run/backend.sock`, but the backend is failing to start and bind correctly. 

Your task is to fix the configuration, harden the deployment, and establish process supervision.

Complete the following steps:

1. **Fix the Backend Code**: 
   The source code for the backend is located at `/home/user/backend.c`. It is currently configured with the wrong socket path (`/home/user/run/old_socket.sock`). Modify `/home/user/backend.c` to use the correct socket path: `/home/user/run/backend.sock`.
   
2. **Compile the Code**: 
   Compile the updated `backend.c` into an executable named `/home/user/backend` using `gcc`.

3. **Harden the Environment**:
   The directory `/home/user/run` does not exist and needs to be created. Create it and set its permissions to strictly `700` to prevent unauthorized local access.

4. **Implement Process Supervision**:
   Write a bash script at `/home/user/supervisor.sh` that acts as a process supervisor. The script must:
   - Run the `/home/user/backend` executable in the foreground.
   - If the backend process crashes or exits, the script should automatically restart it (an infinite loop).
   - Redirect all standard output and standard error from the backend to `/home/user/backend.log`.
   Make the script executable and start it in the background using standard shell job control (e.g., `nohup /home/user/supervisor.sh &`).

5. **Verify the Deployment**:
   Send the string "PING" to the UNIX socket `/home/user/run/backend.sock` (using `nc -U` or `socat`) and save the response from the daemon to `/home/user/response.txt`.

Ensure all file paths match exactly as requested. Do not change the underlying C logic other than the socket path.