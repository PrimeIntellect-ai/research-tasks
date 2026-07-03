You are a performance engineer profiling a spectroscopy signal processing pipeline. The pipeline processes streams of spectral intensities, but it currently yields non-reproducible distribution distance metrics between experimental and theoretical spectra. This instability has been traced to floating-point reduction order issues in the legacy parallel data processor.

Your objective is to fix the pipeline by replacing the buggy summation step with a strictly deterministic and exact reduction, and then reconfigure the microservices to communicate correctly.

Step 1: Create a Deterministic Processor
Write a program at `/home/user/processor` (make sure it is executable). It must:
- Read a sequence of space-separated floating-point numbers from standard input (until EOF).
- Compute their exact sum to eliminate floating-point rounding variations. You must use an exact summation algorithm (for instance, Python's `math.fsum` or a mathematically equivalent exact partial-sum accumulator).
- Print ONLY the final sum to standard output, formatted to exactly 6 decimal places (e.g., `printf("%.6f\n", sum)`).

Step 2: Reconfigure and Compose Services
The pipeline consists of three services:
1. Redis (already running on `127.0.0.1:6379`)
2. Spectroscopy Emitter (Flask app)
3. Metric Analyzer (Flask app)

The source and configuration files for the Emitter and Analyzer are located in `/home/user/services/`.
Currently, the pipeline is broken:
- The Emitter's config (`/home/user/services/emitter/config.env`) specifies the wrong Redis port (it points to 6380 instead of 6379).
- The Analyzer's config (`/home/user/services/analyzer/config.env`) is missing the path to the processing executable and also has the wrong Redis port. 

You must:
- Edit `/home/user/services/emitter/config.env` to set `REDIS_PORT=6379`.
- Edit `/home/user/services/analyzer/config.env` to set `REDIS_PORT=6379` and `PROCESSOR_PATH=/home/user/processor`.

Step 3: Verification
Once the configurations are corrected, start the Emitter and Analyzer services (they can be started via their respective `app.py` scripts or a runner script if present). 
The Analyzer provides an endpoint at `http://127.0.0.1:5001/analyze` that triggers the pipeline: it commands the Emitter to generate signal batches, processes them through your `/home/user/processor`, and returns the Kullback-Leibler (KL) divergence metric. Ensure this endpoint returns an HTTP 200 OK and a valid JSON response containing the metric.