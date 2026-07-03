You are acting as a system administrator tasked with fixing a broken deployment in a local CI/CD environment. 

Our Nginx reverse proxy is currently returning a `502 Bad Gateway` error when accessing `http://127.0.0.1:8080`. 

The deployment relies on a pipeline script located at `/home/user/cicd/deploy.sh`, which is supposed to start a Python backend service located at `/home/user/app/server.py`. 

The local Nginx instance uses the configuration file at `/home/user/nginx/nginx.conf` (running in user space).

Your task is to:
1. Identify and resolve the cause of the `502 Bad Gateway` error.
2. Fix any misconfigurations in the Python application, the deployment script, or the Nginx configuration. Nginx expects to proxy requests to the application.
3. Ensure the deployment script `/home/user/cicd/deploy.sh` successfully starts the backend in the background.
4. Once the service is running and properly proxied by Nginx, create a Python script at `/home/user/verify.py` that makes an HTTP GET request to `http://127.0.0.1:8080` and writes the exact response text to `/home/user/success.log`.

Do not change the Nginx listening port (8080). You must start the Nginx server and the backend application before running your verification script. Nginx can be started with `nginx -c /home/user/nginx/nginx.conf`.