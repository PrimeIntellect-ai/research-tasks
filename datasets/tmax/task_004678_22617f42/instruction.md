You are acting as a data scientist and systems engineer. We are deploying a reproducible computation pipeline to process incoming Raman spectroscopy data. You need to write a Go-based signal processing filter and integrate it into our multi-service ingestion pipeline.

Our spectroscopy sensors occasionally produce bad data due to thermal baseline drift or weak signal-to-noise ratios. Your task is to build a filter to reject these bad signals and configure our ingestion services to use it.

**Step 1: Write the Statistical Filter in Go**
Create a Go program at `/home/user/spectro_filter.go` and compile it to `/home/user/spectro_filter`.
This CLI must accept a single command-line argument: the path to a JSON file containing the spectral data.
The JSON format is:
`{"x": [array of floats], "y": [array of floats]}`
(Assume both arrays are exactly 1000 elements long).

Your Go program must parse this file and evaluate the spectrum against two hypothesis tests. To do this, isolate a "baseline region" consisting of the first 50 points (indices 0 to 49) and the last 50 points (indices 950 to 999) of the arrays.

1. **Baseline Drift Test (Curve Fitting / Regression):** Perform a simple linear regression ($y = mx + c$) on the 100 points of the baseline region (using their actual `x` and `y` values). If the absolute value of the slope $|m|$ is strictly greater than `0.05`, the spectrum has too much drift.
2. **Signal-to-Noise Test (Statistical Analysis):** Calculate the mean ($\mu$) and sample standard deviation ($s$) of the `y` values within those same 100 baseline points. Find the absolute maximum `y` value in the *entire* 1000-point spectrum. If this maximum peak is strictly less than $\mu + (5 \times s)$, the spectrum lacks a statistically significant peak.

If the spectrum FAILS either of these tests, your program must exit with status code `1` (rejected). If it passes both, it must exit with status code `0` (accepted).

You can test your compiled binary against the provided datasets:
- `/app/corpora/clean/` (10 files, all should exit 0)
- `/app/corpora/evil/` (10 files, all should exit 1)

**Step 2: Fix the Multi-Service Composition**
Our backend pipeline consists of a Redis cache and a Python data ingestion API.
1. Start a local Redis server on its default port (6379).
2. The ingestion service is located at `/app/services/ingest.py`. Before starting it, you must configure it by editing `/app/services/config.yaml`.
   Update the configuration file so that:
   - `redis_host` is set to point to your local Redis instance.
   - `redis_port` is set to `6379`.
   - `filter_bin` is set to the absolute path of your compiled Go binary (`/home/user/spectro_filter`).
3. Start the Python ingestion API (it runs on port 8000). Leave it running in the background.

The ingestion API receives HTTP POST requests with spectral JSON. It shells out to your Go binary. If the Go binary exits with 0, the API stores the JSON payload into a Redis list named `valid_spectra`.

Verify your setup by running the services and ensuring the API correctly processes payloads and routes them to Redis only when valid.