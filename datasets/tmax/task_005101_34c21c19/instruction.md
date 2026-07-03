You are an AI assistant helping a bioinformatics researcher debug and deploy a local simulation pipeline for a biological data storage project. The project involves screening synthesized DNA sequences to detect "adversarial" or corrupted sequences before they enter the data store.

We have a multi-service pipeline located in `/app/dna_pipeline/` that consists of:
1. A Redis cache/queue.
2. A Flask API (`api.py`) that receives sequences.
3. A Background Worker (`worker.py`) that evaluates the sequences.

Unfortunately, the pipeline is currently broken and the sequence evaluation logic is missing. Your task is to fix the environment, configure the services, and implement the classification logic.

### Step 1: Environment and Configuration
1. Activate or set up a Python environment with necessary packages (e.g., `flask`, `redis`, `numpy`, `scipy`).
2. Fix `/app/dna_pipeline/config.yaml` so the services can communicate. The Flask API should run on port `5000`, Redis on port `6379`, and the Worker should point to the Redis instance.
3. Use `/app/dna_pipeline/start.sh` to bring up the Redis server, Flask API, and Worker process in the background. Ensure they stay running.

### Step 2: Implement the Classifier
Implement the `evaluate_sequence(dna_string)` function inside `/app/dna_pipeline/classifier.py`. The worker uses this function. It must return `"clean"` or `"evil"`.

The criteria for a sequence to be `"clean"` are:
1. **Primer Alignment**: The sequence must start EXACTLY with the 8-bp primer `GCATCGAT`. If it does not, it is `"evil"`.
2. **Spectral Analysis & Bootstrap CI**: After removing the 8-bp primer, convert the remaining DNA sequence to a numerical array using the mapping: `A = 1`, `C = 2`, `G = -1`, `T = -2`.
   - Evil sequences contain a synthetic periodic anomaly of period 5.
   - To detect this, slice the numerical sequence into contiguous, non-overlapping blocks of length 5 (discard any remainder at the end).
   - Generate 1000 bootstrap samples of the sequence by sampling these 5-bp blocks *with replacement* to construct a new sequence of the same block-length.
   - For each bootstrap sample, compute the Discrete Fourier Transform (using `numpy.fft.fft`). Calculate the power spectrum (absolute value squared of the FFT).
   - Extract the power at the frequency bin corresponding exactly to period 5 (i.e., index `len(sample) // 5`).
   - Calculate the 95% confidence interval of this power value across the 1000 bootstrap samples (using the 2.5th and 97.5th percentiles).
   - If the *lower bound* of this 95% CI is strictly greater than `200.0`, the sequence is `"evil"`. Otherwise, it is `"clean"`.

### Step 3: Verify End-to-End
We have provided two corpora of DNA sequences (in `.txt` files, one sequence per file):
- `/app/corpus/clean/`
- `/app/corpus/evil/`

The verifier will exercise the end-to-end flow by sending HTTP POST requests containing JSON `{"sequence": "<dna>"}` to `http://127.0.0.1:5000/classify`. The pipeline processes this asynchronously and the API eventually returns `{"status": "clean"}` or `{"status": "evil"}`.

You must ensure that:
- 100% of the sequences in the `clean/` corpus return `"clean"`.
- 100% of the sequences in the `evil/` corpus return `"evil"`.

Write the code for `classifier.py`, fix `config.yaml`, and start the services. You may use the corpora to test your pipeline locally. Leave the services running on port 5000 and 6379 when you are finished.