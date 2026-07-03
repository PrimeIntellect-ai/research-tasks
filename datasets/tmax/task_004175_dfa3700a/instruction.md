You are a performance engineer profiling a numerical analysis pipeline. Our backend matrix factorization service frequently crashes when it receives near-singular inputs. These problematic inputs are typically time-series signals characterized by extreme spectral anomalies (e.g., highly concentrated high-frequency noise or massive low-frequency offsets) which produce ill-conditioned matrices.

Your objective is to build a Bash-based stability guard and integrate it into our multi-service ingestion pipeline.

**System Architecture:**
Currently, the system is partially configured under `/app/`:
1. **Matrix Service:** A Python API running on `127.0.0.1:8081` that computes matrix factorizations.
2. **CGI Runner:** `fcgiwrap` running on a UNIX socket at `/tmp/fcgiwrap.socket`.
3. **Gateway:** `nginx` listening on `127.0.0.1:8000`.

**Your Tasks:**

1. **Write the Stability Guard (`/home/user/stability_guard.sh`):**
   Write a Bash script that acts as an executable filter. It must read a sequence of floating-point numbers (one per line) from standard input.
   * Your script must analyze the input to detect spectral anomalies that lead to numerical instability. You should apply a Fast Fourier Transform (you may use lightweight shell tools, `awk`, or call out to a short inline Python/NumPy snippet to compute the FFT and extract the power spectrum).
   * Calculate a Bootstrap Confidence Interval (95%) for the mean power of the upper half of the frequency spectrum. 
   * If the lower bound of this confidence interval exceeds `15.0`, or if the condition number of the signal is deemed highly unstable, reject the input by exiting with status code `1` (or outputting an error for CGI).
   * If the signal is stable, exit with status code `0` (or output the valid proxy response).

2. **CGI Wrapper (`/home/user/cgi_proxy.sh`):**
   Wrap your stability guard in a Bash CGI script. When an HTTP POST request is received:
   * Read the request body.
   * Pass it to `stability_guard.sh`.
   * If rejected, return an HTTP `400 Bad Request` with the body `REJECTED`.
   * If accepted, use `curl` to forward the body to `http://127.0.0.1:8081/factorize`, and return its HTTP `200 OK` response to the client.

3. **Configure Nginx (`/home/user/nginx.conf`):**
   Write an Nginx configuration file that:
   * Listens on port `8000`.
   * Routes all POST requests to `/api/process` to your CGI proxy via `fcgiwrap` at `/tmp/fcgiwrap.socket`.
   * Ensure necessary fastcgi params are included so the script can read the request body.

**Validation:**
We have two corpora of raw signal data:
* `/app/data/clean/`: Contains 50 stable signals.
* `/app/data/evil/`: Contains 50 signals with adversarial spectral properties that crash the backend.

You must ensure that:
* The Nginx service is running with your configuration (`sudo nginx -c /home/user/nginx.conf`).
* The end-to-end pipeline allows 100% of the clean corpus to pass and return an HTTP 200, while 100% of the evil corpus returns HTTP 400.