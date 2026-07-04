You are a Data Engineer building an ETL and inference pipeline. Our setup consists of a Python service that provides raw data, a Rust microservice that performs Bayesian inference to predict outcomes, and an Nginx API gateway that exposes the endpoints.

Currently, the pipeline is broken and we are not getting the correct predictions from the gateway. 

Here is the setup located in `/app/`:
1. `data_server.py`: Runs on `127.0.0.1:8000` and serves a dataset at `/data.csv` (schema: `x,y`).
2. `inference_service`: A Rust web service located in `/app/inference_service`. It is supposed to fetch `/data.csv` on startup, extract features (we just use `x`), and compute the posterior distribution for a simple 1D Bayesian linear regression model without intercept ($y = w \cdot x + \epsilon$). It assumes a known noise variance $\sigma^2 = 2.0$ and a prior for $w \sim \mathcal{N}(0, 1.0)$. It listens on `127.0.0.1:8080` and exposes a `/predict?x=<val>` endpoint that returns a JSON: `{"mean": <val>, "variance": <val>}` representing the predictive distribution for $y$.
3. `nginx.conf`: An Nginx configuration file meant to proxy requests from `127.0.0.1:80` (endpoint `/api/predict`) to the Rust service.

Your task:
1. Identify and fix the routing misconfiguration in `/app/nginx.conf`. The endpoint `http://127.0.0.1:80/api/predict` should proxy to `http://127.0.0.1:8080/predict`.
2. The Rust service's Bayesian inference logic has a mathematical flaw causing numerical inaccuracy in the posterior variance calculation. In `/app/inference_service/src/main.rs`, locate the posterior computation and fix it. (Recall that for Bayesian linear regression $y = wx + \epsilon$ with prior variance $V_0$ and noise variance $\sigma^2$, the posterior precision is $V_n^{-1} = V_0^{-1} + \sum \frac{x_i^2}{\sigma^2}$ and posterior mean is $w_n = V_n \sum \frac{x_i y_i}{\sigma^2}$. The predictive distribution for a new $x_*$ has mean $w_n x_*$ and variance $x_*^2 V_n + \sigma^2$).
3. Start the `data_server.py` in the background.
4. Start Nginx using the local config: `nginx -c /app/nginx.conf`.
5. Compile and run the Rust service in the background.

Ensure that a `curl http://127.0.0.1:80/api/predict?x=3.0` returns the correct JSON with `mean` and `variance` fields. Do not modify the data in `/data.csv` or the data server.