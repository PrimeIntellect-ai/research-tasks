I am an infrastructure engineer trying to automate the provisioning of a local data pipeline environment. I have two microservices written in Python that need to run continuously, but the environment is currently unconfigured and there is a network mismatch preventing them from communicating. 

The two services are located at:
- `/home/user/src/service_a.py` (Data provider)
- `/home/user/src/service_b.py` (Data consumer)

Here is what you need to do to fix the setup:

1. **Directory Structure & Links:**
   Create the following directory structure:
   - `/home/user/app/data`
   - `/home/user/app/logs`
   
   The consumer service (`service_b.py`) expects to read from and write to `/home/user/app/active_data`. Create a symbolic link at `/home/user/app/active_data` that points to the `/home/user/app/data` directory.

2. **Fix Network Misconfiguration:**
   `service_a.py` runs an HTTP server on `127.0.0.1:8000`. However, `service_b.py` is misconfigured and tries to fetch data from `127.0.0.1:9090`. 
   Modify `/home/user/src/service_b.py` (using Python, sed, or any editor) to connect to the correct port (`8000`).

3. **Process Supervision Configuration:**
   We need to ensure both services stay running. Create a `supervisord` configuration file at `/home/user/app/supervisord.conf` with the following requirements:
   - A `[supervisord]` section with `nodaemon=false`, `logfile=/home/user/app/logs/supervisord.log`, and `pidfile=/home/user/app/supervisord.pid`.
   - A `[program:service_a]` section that runs `python3 /home/user/src/service_a.py`. It must automatically restart on failure (`autorestart=true`), and redirect standard output to `/home/user/app/logs/service_a.log` and standard error to `/home/user/app/logs/service_a.err`.
   - A `[program:service_b]` section that runs `python3 /home/user/src/service_b.py`. It must also automatically restart (`autorestart=true`), with stdout to `/home/user/app/logs/service_b.log` and stderr to `/home/user/app/logs/service_b.err`.
   - Include `[unix_http_server]`, `[rpcinterface:supervisor]`, and `[supervisorctl]` sections with a socket at `/home/user/app/supervisor.sock` so `supervisord` can run cleanly without root.

4. **Start the Services:**
   Start the services by running `supervisord -c /home/user/app/supervisord.conf`. 

Once running successfully and communicating, `service_b.py` will process the data from `service_a.py` and create a file named `pipeline_success.json` inside the data directory (`/home/user/app/data/pipeline_success.json`). Leave the services running in the background when you are done.