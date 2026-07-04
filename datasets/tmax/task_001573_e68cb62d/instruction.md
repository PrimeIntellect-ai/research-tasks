You are a bioinformatics analyst working on a pipeline to filter out synthetically anomalous DNA sequences (which have artificial periodicities introduced) from natural genomic data.

We have a local multi-service architecture that performs statistical hypothesis testing on spectral data, but it is currently broken. You need to repair the pipeline, compile the necessary scientific software, and write a Bash script to act as the primary filter.

### System Components
1. **Multi-Service Backend (in `/app/services/`)**
   - **Redis**: Runs on port 6379, used for caching background spectral distributions.
   - **Flask API**: Located in `/app/services/api/app.py`. It provides an endpoint `POST /analyze_spectrum` which accepts a JSON list of power spectrum values and returns a statistical test result (a p-value indicating if there is an anomalous periodicity). It runs on port 5000.
   - **Nginx**: Acts as the reverse proxy for the API. Its configuration is at `/app/services/nginx/nginx.conf`. It should listen on port 8080 and route `/api/` requests to the Flask app.
   A startup script `/app/services/start_services.sh` brings these up, but the end-to-end flow is failing because Nginx is misconfigured.

2. **Spectral Analysis Tool (in `/home/user/src/`)**
   - We have C source code `calc_spectrum.c` that reads a 1D numeric array from an HDF5 file (dataset name `/sequence`), computes its Fast Fourier Transform (FFT) power spectrum, and prints the power values as a comma-separated string.
   - You must install the necessary development libraries and compile this tool to `/home/user/bin/calc_spectrum`.

### Your Objectives

**1. Fix the Services**
- Identify and fix the misconfiguration in `/app/services/nginx/nginx.conf`.
- Ensure Nginx, Redis, and the Flask API are running correctly. You can restart the services using `/app/services/start_services.sh`.

**2. Compile the Scientific Software**
- Install the required packages to compile C code with HDF5 and FFTW3 support.
- Compile `/home/user/src/calc_spectrum.c` into an executable at `/home/user/bin/calc_spectrum`.

**3. Write the Classifier Script**
- Create a Bash script at `/home/user/filter_seqs.sh`.
- The script must take exactly two arguments: an input directory and an output directory.
  `Usage: /home/user/filter_seqs.sh <input_dir> <output_dir>`
- For every `.h5` file in the `<input_dir>`:
  - Run `calc_spectrum` on the file to get the power spectrum string.
  - Send this string to the local API via Nginx (`http://127.0.0.1:8080/api/analyze_spectrum`) in the following JSON format: `{"spectrum": [val1, val2, ...]}`.
  - Parse the returned JSON to extract the `p_value`.
  - A sequence is considered "evil" (synthetic anomaly) if the `p_value` is STRICTLY LESS than `0.01`. Otherwise, it is "clean" (natural).
  - If the sequence is "clean", copy the `.h5` file to the `<output_dir>`. If it is "evil", ignore it.

The automated verifier will call your script to process two hidden corpora of HDF5 sequences (one entirely clean, one entirely evil) and will check if your script perfectly separates them.