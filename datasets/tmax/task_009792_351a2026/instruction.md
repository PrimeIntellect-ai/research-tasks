You are a platform engineer tasked with fixing a broken CI/CD pipeline step for a legacy log processing microservice.

The workspace is located at `/home/user/workspace`. Inside it, you will find a broken Python package `log-merger`, some raw logs, and a template for a reverse proxy.

Your objectives:

1. **Fix the Python Package Build (Code Translation & Building)**
   The package at `/home/user/workspace/log-merger` fails to build because its `setup.py` is broken and it relies on a C extension (`fast_hash.c`) that is incomplete. 
   - Read `/home/user/workspace/log-merger/reference.py`, which contains the reference implementation of a simple hashing function in Python.
   - Complete the C extension `fast_hash.c` by translating this Python logic into the provided C skeleton.
   - Fix `setup.py` so it properly defines and builds the `fast_hash` C extension module.
   - Install the package locally using `pip install .` inside the `log-merger` directory.

2. **Process and Diff Logs (Sorting, Merging, Diffing)**
   - Once installed, the package provides a CLI command: `python3 -m log_merger <file1> <file2> ...`
   - Use it to merge `/home/user/workspace/logs/serverA.log` and `/home/user/workspace/logs/serverB.log`. The output should be redirected to `/home/user/workspace/output/merged.log`. The tool automatically sorts them by timestamp.
   - Use the standard `diff` command to compare `/home/user/workspace/output/merged.log` against `/home/user/workspace/logs/baseline.log`. Save the diff output to `/home/user/workspace/output/diff.txt`. (Do not worry if `diff` exits with a non-zero status; just capture the standard output).

3. **Configure the Reverse Proxy (Nginx)**
   - We need to expose the `output` directory via an Nginx reverse proxy for the CI system to download the artifacts.
   - Start a simple Python HTTP server on port `9000` serving the `/home/user/workspace/output` directory.
   - Create an Nginx configuration file at `/home/user/workspace/nginx.conf`. It must:
     - Run as the current non-root user (do not use `user` directive).
     - Store its pid and client temp files inside `/home/user/workspace/nginx_temp/` to avoid permission errors.
     - Listen on port `8080`.
     - Reverse proxy all requests (`/`) to the Python HTTP server running on `127.0.0.1:9000`.
   - Start Nginx using your custom configuration: `nginx -c /home/user/workspace/nginx.conf`.

At the end of your task, I should be able to run `curl -s http://127.0.0.1:8080/diff.txt` and get the diff file you generated.