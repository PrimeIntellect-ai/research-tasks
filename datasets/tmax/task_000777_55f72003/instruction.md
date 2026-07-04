You are a network engineer tasked with troubleshooting and fixing a severe performance issue with a custom internal reverse proxy. Users are complaining that connections passing through the proxy are incredibly slow and often time out.

We have provided the source code for the proxy, a Python package named `fast-forwarder`, located in the `/app/fast-forwarder` directory. It is supposed to handle TLS termination and forward requests to a backend HTTP server, but its throughput is currently abysmal.

Your objectives:
1. **Debug and Fix the Proxy**: Identify and fix the performance bottleneck in the `/app/fast-forwarder` package. 
2. **Idempotent Deployment Script**: Write a shell script at `/home/user/deploy.sh` that fully sets up the environment and starts the services. The script must be strictly idempotent (it should be safe to run multiple times consecutively without crashing or duplicating processes). 
   
The `/home/user/deploy.sh` script must perform the following actions:
- Create the directory `/home/user/tls/` if it does not exist.
- Generate a self-signed TLS certificate (`/home/user/tls/cert.pem`) and private key (`/home/user/tls/key.pem`). This generation must require no interactive prompts.
- Create a Python virtual environment at `/home/user/venv`.
- Install the patched `fast-forwarder` package into this virtual environment.
- Create a directory `/home/user/www/` containing an `index.html` file with the exact text `OK`.
- Start a basic background Python HTTP server running on `127.0.0.1:8080` that serves the contents of `/home/user/www/`. Make sure old instances are killed gracefully if the script is re-run.
- Start the `fast-forwarder` proxy daemon in the background using the virtual environment. It should listen on `127.0.0.1:8443` with TLS enabled using the generated cert/key, and forward traffic to the backend server at `127.0.0.1:8080`. The command to run the proxy (once installed) is `fast-forwarder --bind 127.0.0.1 --port 8443 --cert /home/user/tls/cert.pem --key /home/user/tls/key.pem --forward 127.0.0.1:8080`.

Once you have written the script, execute it to ensure the environment is running. Finally, make sure the backend web server and the reverse proxy are successfully running and accepting connections.