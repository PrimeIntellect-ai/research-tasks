You are assisting a researcher who is running numerical simulations of a stochastic integrator. Due to step-size adaptation issues, the integrator sometimes diverges. The researcher has built a local microservice stack to serve the historical divergence error data, but the stack is currently misconfigured.

Your goal is to fix the microservice stack, retrieve the data, and write a Go utility to compute a bootstrap confidence interval for the mean divergence error.

**Part 1: Fix the Microservices**
The microservice stack is located in `/app/` and is started via `/app/start_services.sh`. It consists of:
1.  A Redis instance (stores the raw simulation errors).
2.  An API server (`/app/api_server`) that reads from Redis and serves data via HTTP.
3.  An Nginx reverse proxy (configured via `/app/nginx/nginx.conf`) listening on port 8080.

Currently, if you run `/app/start_services.sh` and try to `curl http://localhost:8080/dataset`, it fails. 
1. The API server expects the `REDIS_PORT` environment variable to match the running Redis instance, but `start_services.sh` launches Redis on its default port and sets the wrong port in the environment.
2. The Nginx configuration points to the wrong upstream port for the API server (the API server listens on 9000).
Fix these configurations, restart the services, and download the data to `/home/user/dataset.txt` via `curl -s http://localhost:8080/dataset > /home/user/dataset.txt`.

**Part 2: Write the Bootstrap Utility in Go**
Write a Go program at `/home/user/bootstrapper.go` and compile it to `/home/user/bootstrapper`.
The program must take exactly two command-line arguments: `<seed>` (an int64) and `<B>` (an int, the number of bootstrap samples).

It must do the following exactly to ensure reproducibility:
1. Read the floats from `/home/user/dataset.txt` (one per line). Let this be dataset $D$ of size $N$.
2. Initialize the Go random number generator using `math/rand.New(math/rand.NewSource(seed))`.
3. Generate $B$ bootstrap samples. For each bootstrap sample $b$ (from $0$ to $B-1$):
   a. Sample $N$ items from $D$ with replacement. To pick an index, use `rand.Intn(N)`. Sample exactly $N$ times per bootstrap iteration in order.
   b. Compute the mean of these $N$ items.
4. Sort the $B$ resulting means in ascending order.
5. Compute the 95% confidence interval using the percentile method. The lower bound index is exactly `int(0.025 * float64(B))` and the upper bound index is exactly `int(0.975 * float64(B))`.
6. Print the result to standard output in exactly this format:
   `CI: [<lower_bound>, <upper_bound>]` (formatted to 4 decimal places, e.g., `CI: [1.2345, 2.3456]`).

Ensure your compiled binary is at `/home/user/bootstrapper`.