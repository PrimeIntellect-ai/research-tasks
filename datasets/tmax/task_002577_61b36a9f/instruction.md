You are a FinOps analyst tasked with load-testing a new cost-saving API routing architecture. To ensure accurate benchmarks, you must set up a local CI/CD pipeline, fix a misconfigured Docker Compose environment, compile a vendored load-testing tool, and route traffic securely via an SSH tunnel.

Here are your instructions:

1. **Fix the Load Testing Tool:**
   You have the source code for the `wrk` HTTP benchmarking tool vendored at `/app/wrk`. Currently, running `make` fails due to a missing library linkage in the `Makefile`. Identify the missing standard C library (hint: it fails on math functions) and fix the Makefile so `wrk` compiles successfully. Leave the compiled `wrk` binary at `/app/wrk/wrk`.

2. **Fix the Docker Compose Environment:**
   In `/home/user/deploy`, there is a `docker-compose.yml` containing an `nginx` reverse proxy and an `api` backend. Currently, Nginx returns a 502 Bad Gateway because it cannot reach the API. They are isolated on different Docker networks (`front-tier` and `back-tier`). Fix the Docker Compose configuration so `nginx` can route requests to `api`. The host port for Nginx is `9090`.

3. **Set up the CI/CD Pipeline:**
   - Create a bare Git repository at `/home/user/git/api.git`.
   - Write a Git `post-receive` hook (using Bash) that checks out the latest pushed code into `/home/user/deploy` and automatically runs `docker compose up -d --build` inside that directory.
   - Commit the fixed `docker-compose.yml` to a local clone and push it to the bare repository to trigger a successful deployment.

4. **Establish an SSH Tunnel:**
   Set up a local SSH tunnel that forwards your local port `8080` to the Nginx host port `9090` (e.g., `ssh -L 8080:127.0.0.1:9090 ...`). Ensure this tunnel runs in the background.

Once finished, your system should be able to serve traffic on `http://127.0.0.1:8080`, and running `/app/wrk/wrk -c 10 -t 1 -d 5s http://127.0.0.1:8080` should succeed with high throughput and no socket errors.