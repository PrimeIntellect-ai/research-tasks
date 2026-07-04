You are tasked with fixing a web service that is currently returning a 502 Bad Gateway error. 

We have an Nginx reverse proxy configured in `/home/user/nginx.conf` (running on port 8080) that is supposed to forward traffic to a backend service. The backend service is a Bash-based HTTP server located at `/home/user/backend.sh`. However, the backend is highly unstable and exits frequently, causing the 502 errors. Furthermore, the previous administrator made some changes before leaving, and the backend now refuses to run correctly due to a missing specific user account and a port mismatch.

You have been provided with a screen recording of the previous administrator's terminal session right before the system broke, located at `/app/incident_log.mp4`. 

Your objectives are:
1. **Analyze the Video**: Extract frames from `/app/incident_log.mp4` to discover the specific username the backend expects to run as, and the correct internal port it expects to bind to.
2. **System Administration**: 
    - Create the required user account (with no login shell and a locked password) based on the video's contents.
    - Update the Nginx configuration (`/home/user/nginx.conf`) to forward traffic to the correct backend port discovered in the video.
3. **Process Supervision**: 
    - Write a Bash supervisor script at `/home/user/supervisor.sh`.
    - This script must continuously run `/home/user/backend.sh` *as the newly created user*.
    - Because the backend simulates crashes frequently, your supervisor must instantly restart it whenever it exits.
4. **Service Startup**: 
    - Start your supervisor script in the background.
    - Start Nginx using the local config file: `nginx -c /home/user/nginx.conf`.

The automated verification system will send 100 concurrent/sequential requests to the Nginx endpoint (`http://127.0.0.1:8080/`). Your setup will be evaluated on its reliability. To pass, the success rate (HTTP 200 OK) must be evaluated as a numerical metric, and you must achieve a success rate of >= 95%.