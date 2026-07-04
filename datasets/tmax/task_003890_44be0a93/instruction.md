You are acting as a network engineer troubleshooting connectivity for our new local environment.

We have a multi-service stack running in `/app/`. It consists of:
1. An Nginx reverse proxy listening on `127.0.0.1:8080`.
2. A Python Flask API served by Gunicorn.
3. A QEMU virtual machine that the API communicates with via a serial UNIX socket.

Currently, we are facing several issues:
1. Whenever we make a request to `http://127.0.0.1:8080/api/status`, we receive a "502 Bad Gateway" error.
2. The QEMU VM is supposed to be launched using `/app/start_vm.sh`, but the API is complaining about missing or inaccessible socket connections to the VM.
3. Once the functional errors are fixed, the service performs poorly under load.

Your objectives:
1. Fix the Nginx configuration (`/app/nginx/nginx.conf`) and/or the Gunicorn configuration (`/app/api/gunicorn.conf.py`) so that Nginx correctly proxies requests to the Python API. 
2. Fix `/app/start_vm.sh` so that QEMU creates a serial socket at `/app/run/qemu.sock` that the Python API can read from and write to. Ensure proper socket permissions are set so the API process can access it.
3. Optimize the Nginx and Gunicorn configurations to increase performance.
4. Ensure all services are running and functioning. Start Nginx, Gunicorn, and the QEMU VM.

To verify your performance fix, we will run the provided `/app/benchmark.py` script. The verifier will execute this script, which outputs a line like `Throughput: 150.5 req/s`. You must tune the configurations (e.g., worker processes, threads, nginx worker connections) such that the throughput is greater than or equal to 300.0 req/s.

All commands and configurations should use standard built-in tools. You do not have root access, but you have full permissions within `/app/`.