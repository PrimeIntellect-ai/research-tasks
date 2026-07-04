You are helping a computational biology researcher debug and wrap a legacy simulation tool. The tool simulates an NMR-like spectrometer signal from a protein sequence, but it suffers from non-reproducible outputs due to floating-point reduction order issues in its multithreaded core.

You need to build a Python-based HTTP API that handles incoming structural data, runs the simulation multiple times to average out the non-determinism, performs signal processing, compares the results against a reference dataset statistically, and returns the analysis.

Here are the requirements:
1. There is a compiled, stripped binary located at `/app/sim_spectrometer`. 
   Usage: `/app/sim_spectrometer <input.fasta> <output.csv>`
   It generates a time-domain signal CSV with two columns: `time` and `amplitude`.

2. Write a Python HTTP service (using any framework like Flask or FastAPI) that listens on `127.0.0.1:8000`.

3. The service must expose a POST endpoint at `/process` that accepts JSON in the format:
   `{"pdb_data": "<string containing raw PDB file content>"}`

4. When the endpoint is called, your service must:
   a. Parse the `pdb_data` to extract the protein sequence (use the `SEQRES` records) and format it as a standard FASTA file. Save it to a temporary file. (Assume single chain).
   b. Run the `/app/sim_spectrometer` binary on this FASTA file exactly 15 times to generate 15 distinct signal CSVs.
   c. For each of the 15 signals:
      - Read the time-domain signal.
      - Perform a Fast Fourier Transform (FFT) to convert it to the frequency domain (assume a sampling rate of 1000 Hz, meaning `time` goes in steps of 0.001s).
      - Identify the "dominant frequency" (the positive frequency > 0 Hz with the highest magnitude).
   d. Read the reference dominant frequencies from `/app/reference_freqs.csv` (which contains a single column of floating-point frequency values).
   e. Perform a Welch's 2-sample t-test comparing your 15 computed dominant frequencies against the reference frequencies.
   f. Return a JSON response in this exact format:
      `{"mean_dominant_freq": <float>, "p_value": <float>}`

5. The service must remain running in the foreground or be started as a background process so that automated tests can query it. Start your service and leave it running.

You may install any Python packages you need (e.g., `biopython`, `scipy`, `numpy`, `flask`).