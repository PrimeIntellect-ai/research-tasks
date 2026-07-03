You are an ML Engineer responsible for a data ingestion pipeline. We receive batches of sensor data for training, but our models are being poisoned by anomalous (adversarial) sensor readings. 

Your task involves two main parts: fixing the multi-service data ingestion pipeline, and writing a fast, parallelized Bash script to filter out the malicious data.

**Part 1: Multi-Service Pipeline Repair**
Under `/app/pipeline/`, there are three services meant to work together to process incoming data:
1. A Redis server instance.
2. A Python Flask API (`/app/pipeline/api.py`) that receives HTTP POST requests containing file paths and pushes them to a Redis queue named `task_queue`.
3. A Bash worker daemon (`/app/pipeline/worker.sh`) that continuously pops file paths from `task_queue` and passes them to our filter script.

Currently, the services are misconfigured. The Redis server is not listening on the correct socket/port, the Python API is pointing to the wrong Redis host, and the worker script is using the wrong Redis command to pop tasks. 
- You must configure Redis to listen on `127.0.0.1:6379`.
- You must fix `api.py` and `worker.sh` so that when a path is POSTed to `http://127.0.0.1:8080/ingest`, the worker correctly receives it and executes `/app/filter.sh <path>`.
- Make sure to start all three services in the background.

**Part 2: Adversarial Data Filter**
You must write the missing script `/app/filter.sh`. This script will act as an adversarial filter for the data files.
Each data file contains 1,000 floating-point numbers (one per line).
"Clean" data is drawn from a distribution with a true mean of 50.0.
"Evil" (poisoned) data is drawn from a shifted distribution.

To robustly identify evil data, your `/app/filter.sh` script must perform a **Bootstrap Confidence Interval** estimation via Monte Carlo simulation using Bash and utilities like `awk` and GNU `parallel`:
1. Take the input file path as `$1`.
2. Perform exactly 500 bootstrap iterations. In each iteration, sample 1,000 lines *with replacement* from the input file and calculate the mean of that sample.
3. Use GNU `parallel` to parallelize these 500 iterations across available CPU cores for speed.
4. Calculate the 2.5th percentile and 97.5th percentile of these 500 bootstrap means to form a 95% confidence interval.
5. If the value `50.0` falls *within or exactly on* the bounds of this interval, output exactly `ACCEPT` to standard output.
6. If the value `50.0` falls *outside* the interval (i.e., strictly less than the lower bound or strictly greater than the upper bound), output exactly `REJECT` to standard output.

Your script must be robust, executable, and heavily optimized via `parallel`. You can test your filter locally. Once complete, leave the services running. The automated verifier will test your pipeline and the accuracy of your `/app/filter.sh` on a hidden corpus.