You are an SRE on call. Our primary monitoring dashboard is showing an outage. The NGINX reverse proxy is returning a 502 Bad Gateway error when accessed. 

An automated emergency voicemail from the lead engineer has been saved to `/app/emergency_voicemail.wav`. You have access to `whisper` in your path to transcribe this file.

Your tasks are:
1. Transcribe `/app/emergency_voicemail.wav`. It contains the correct UNIX socket path for our backend service, as well as a secret authorization token.
2. The current NGINX configuration is located at `/home/user/nginx/nginx.conf`. Before making any changes, create a tarball backup of this directory at `/home/user/nginx_backup.tar.gz`.
3. Fix the NGINX configuration so that it proxies requests to the correct UNIX socket mentioned in the audio file.
4. Update the NGINX configuration to require the secret authorization token (also mentioned in the audio) as a Bearer token in the `Authorization` HTTP header. If the header is missing or incorrect, NGINX must return a 401 Unauthorized status. 
5. The backend service is currently stopped. Use the custom init script at `/home/user/init_backend.sh` to start the service (`/home/user/init_backend.sh start`). This script creates the socket and starts the daemon.
6. Start NGINX using the local configuration: `nginx -c /home/user/nginx/nginx.conf`. The NGINX server is configured to listen on `127.0.0.1:8080`.

Ensure the service is up, running, and correctly handling requests before finishing.