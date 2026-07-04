You are a data scientist debugging a high-performance scientific computing pipeline. We have a multi-service architecture located in `/home/user/app/` that performs bootstrap confidence interval estimation and linear regression on Monte Carlo simulated data. 

Currently, the pipeline is failing our reproducibility tests. The backend analysis engine, written in C, uses multiple threads to compute sums for the linear regression model. Because floating-point addition is not associative and the threads add to a shared global variable using a mutex, the order of additions changes on every run. This causes the computed bootstrap confidence intervals to fluctuate slightly, which fails our strict deterministic verification suite.

Your goal is to fix the C code, properly configure the service routing, and bring up the system.

Here are the details of the services:
1. **Data Broker (`/home/user/app/broker.py`)**: A simple Python service that listens on TCP port 9000. When a connection is made, it streams a synthetic dataset of `(x, y)` pairs as binary `float` (IEEE 754 32-bit) arrays and closes the connection.
2. **Analysis Engine (`/home/user/app/engine.c`)**: A C program you need to fix and compile. It listens for basic HTTP GET requests on port 5000. When it receives `GET /analyze HTTP/1.0`, it:
   - Connects to `localhost:9000` to read the dataset.
   - Performs a Monte Carlo bootstrap simulation (10,000 iterations) to estimate the 95% confidence interval of the linear regression slope.
   - Prints the result as an HTTP response.
   *The Bug*: The `engine.c` file uses pthreads. The threads update global sum variables `sum_x`, `sum_y`, `sum_xy`, `sum_xx` directly using a mutex lock. You must modify `engine.c` so that each thread computes local sums, and the main thread aggregates these local sums sequentially by thread ID. This guarantees a deterministic reduction order.
3. **Nginx Frontend**: You must configure an Nginx reverse proxy to expose the analysis engine. 
   - It must listen on port 8080.
   - It must route requests from `http://localhost:8080/api/fit` to the Analysis Engine at `http://localhost:5000/analyze`.
   - It must require an exact HTTP header: `Authorization: Bearer BOOTSTRAP_SECURE_99`. If missing or incorrect, it should return 401.

**Instructions:**
1. Fix the floating point reduction issue in `/home/user/app/engine.c` to be completely deterministic.
2. Compile the fixed C code into `/home/user/app/engine` (link with `-lpthread` and `-lm`).
3. Write the necessary Nginx configuration to `/home/user/app/nginx.conf`.
4. Start the `broker.py` in the background.
5. Start your compiled `./engine` in the background.
6. Start Nginx using your custom config in the background (`nginx -c /home/user/app/nginx.conf`).
7. Verify your setup. When we query `curl -H "Authorization: Bearer BOOTSTRAP_SECURE_99" http://localhost:8080/api/fit`, it should consistently return the exact same output (e.g., `[1.234567, 1.456789]`) down to the 6th decimal place across multiple calls.
8. Create a log file at `/home/user/app/success.log` containing the exact HTTP response body from a successful `curl` call to your Nginx proxy.