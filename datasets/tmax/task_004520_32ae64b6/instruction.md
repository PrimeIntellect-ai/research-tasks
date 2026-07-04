You are a release manager tasked with deploying a lightweight microservice. The service relies on Nginx as a reverse proxy, a Python Flask backend, and a Redis cache. 

Your goals are to resolve the minimal dependencies for the backend application, bundle them into a deployment directory, and bring up the full service stack.

System Setup (already available):
- A Redis instance is running locally on the default port `6379`.
- A source code directory exists at `/app/src/`, containing many Python files and a custom dependency graph file `/app/src/deps.txt`.
- An empty deployment directory exists at `/app/deploy/`.

Task Instructions:
1. Write a Bash script `/home/user/bundle.sh` that implements graph traversal. It must read `/app/src/deps.txt` to find all transitive dependencies of `app.py`. 
   - The format of `deps.txt` is: `filename: dep1, dep2, ...`
   - Your script must parse this file starting from `app.py` and compute the full closure of required files.
   - The script must copy ONLY `app.py` and its resolved dependencies from `/app/src/` to `/app/deploy/`. 
   - Do NOT copy unneeded files. We will strictly measure the total byte size of `/app/deploy/` to ensure you successfully minimized the bundle.

2. Start the Python backend:
   - Run `python3 /app/deploy/app.py` in the background. It will bind to `127.0.0.1:5000` by default.

3. Configure and start Nginx:
   - Create an Nginx configuration file at `/home/user/nginx.conf` that starts Nginx as a non-root user.
   - It should listen on `127.0.0.1:8080`.
   - It must reverse-proxy all HTTP requests to the Flask backend at `127.0.0.1:5000`.
   - Start Nginx using this configuration (`nginx -c /home/user/nginx.conf`).

4. Create a log file at `/home/user/deploy_status.log` containing the word `READY` once you have completed all steps and the services are running.

Constraints:
- Use only standard Bash utilities for the graph traversal.
- The total size of files in `/app/deploy/` must be below the required threshold to pass the automated metric verification.
- You do not have root access. Run Nginx locally using paths you have permission to write to (e.g., put pid files and error logs in `/home/user/`).