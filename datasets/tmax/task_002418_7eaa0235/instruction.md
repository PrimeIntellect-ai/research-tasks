You are an observability engineer tasked with tuning our deployment pipeline for a custom dashboard generation tool. Our CI/CD pipeline is currently failing because the log parsing step takes too long on production workloads, and the container build process is broken. 

We have a vendored package for the tool at `/app/obs-dash-gen` (a Python application). It reads system logs and generates a static HTML dashboard.

Your objectives:
1. **Fix the Package**: The package contains a catastrophic performance issue when parsing edge-case log lines in `/app/obs-dash-gen/parser.py`. Identify the poorly written regular expression or logic and optimize it so it runs efficiently.
2. **Containerize**: Create a `Dockerfile` at `/app/obs-dash-gen/Dockerfile`. It must use a standard Python base image, copy the package, and set the entrypoint to run `main.py`.
3. **CI/CD Pipeline Script**: Write a bash script at `/home/user/run_pipeline.sh` that automates the deployment test. The script must:
    - Build the Docker container with the tag `obs-dash:latest`.
    - Run the container, mounting `/home/user/system.log` (a file containing 50,000 log lines) into the container, and capturing the standard output (which is the generated HTML) to `/home/user/dashboard.html`.
    - Serve the directory locally on port 8080 using Python's `http.server` in the background.
    - Perform a connectivity diagnostic by using `curl` to fetch `http://localhost:8080/dashboard.html` and verify the HTTP 200 response, appending the HTTP status code to `/home/user/deploy_status.txt`.

We will evaluate the performance of your fixed parser. To pass, the parsing of 50,000 log lines must complete in under 2.0 seconds. 

Make sure `/home/user/run_pipeline.sh` is executable and run it to produce the final dashboard.