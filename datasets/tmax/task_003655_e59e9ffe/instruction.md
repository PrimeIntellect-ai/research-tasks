You are a bioinformatics analyst working with raw nanopore sequencing data. We have a local streaming pipeline under `/app/nanopore_pipeline/` that simulates real-time basecalling by integrating raw signal intensities to estimate total charge translocations. 

The pipeline consists of three services that must work together:
1. **Signal Streamer** (`/app/nanopore_pipeline/streamer.py`): A Flask API running on port 5000 that serves raw signal traces (spectroscopy-like time-series data).
2. **Message Queue**: A local Redis instance that must run on port 6379. 
3. **Integration Worker** (`/app/nanopore_pipeline/worker.sh`): A Bash script that pulls signal data IDs from Redis, fetches the signal array from the Flask API, and calculates the total charge over the translocation interval using a numerical integration helper (`/app/nanopore_pipeline/integrate.py`).

**The Problem:**
1. The pipeline is currently misconfigured. The services are not communicating correctly. You need to identify the misconfigurations in the `.env` file and `worker.sh` and ensure the end-to-end flow works: Streamer -> Redis -> Worker -> Output.
2. The current numerical integration implemented in `integrate.py` uses a naive fixed-step Riemann sum. Because the nanopore signals contain extremely sharp, high-frequency peaks, this fixed step-size adaptation is diverging or severely undersampling the peaks, leading to massive errors in the final charge calculations. 

**Your Task:**
1. Fix the multi-service configuration so the pipeline successfully communicates.
2. Modify `integrate.py` (and potentially how `worker.sh` calls it) to implement an adaptive numerical integration strategy (e.g., adaptive mesh refinement, or using robust library functions like Scipy's `quad` or Monte Carlo integration) to accurately integrate the highly variable signal arrays.
3. Start the Redis server, start the Flask streamer in the background, and execute `worker.sh` to process all 100 queued signal events.
4. The worker must output the final integrated values to `/home/user/results.csv` in the format: `event_id,total_charge`.

**Requirements:**
- The final output in `/home/user/results.csv` must precisely map the `event_id` to your computed integral.
- Your integration method must be highly accurate. An automated metric will evaluate the Mean Squared Error (MSE) between your computed charges and the analytical ground truth. 
- You must achieve an MSE of less than 0.05.