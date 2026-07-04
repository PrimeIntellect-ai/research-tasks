I have a local web stack set up in my home directory, but my Nginx reverse proxy is returning a "502 Bad Gateway" when I try to access it. 

The stack consists of a local Nginx instance serving on port 8080 and a backend service that is supposed to be launched by a bash script located at `/home/user/backend/run.sh`. 

Someone else was working on this and left it in a broken state. Could you please fix it?

Here is what you need to do:
1. Examine the backend startup script `/home/user/backend/run.sh`. It currently fails to start because of missing filesystem dependencies and a missing environment variable. 
2. Fix the missing filesystem requirements (the script expects a specific directory to exist).
3. Set the required environment variable persistently by exporting it in `/home/user/.bash_profile`. You can choose any high, unused port number for the backend (e.g., 8081).
4. Start the backend service in the background using the fixed `/home/user/backend/run.sh`.
5. Examine the Nginx configuration at `/home/user/nginx/nginx.conf`. It is currently configured with a typo in the `proxy_pass` directive, and might be pointing to the wrong port anyway. Update it to proxy requests to the exact port you configured in `/home/user/.bash_profile`.
6. Reload the Nginx server so the new configuration takes effect (you can use `nginx -c /home/user/nginx/nginx.conf -s reload`).
7. Finally, test the full stack by running `curl -s http://127.0.0.1:8080` and save the output exactly into a file named `/home/user/success.log`. 

The test will pass if `/home/user/success.log` contains the successful response from the backend server.