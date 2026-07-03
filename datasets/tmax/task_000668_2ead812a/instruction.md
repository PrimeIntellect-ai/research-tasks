You are a performance engineer tasked with building a robust API gateway for a bioinformatics pipeline. We have two backend microservices already written and placed in `/app/`:
1. `/app/aligner.py` (runs on port 5000): Takes a DNA primer and aligns it against a reference genome.
2. `/app/fft.py` (runs on port 5001): Performs a Fast Fourier Transform (FFT) on the sequence's numerical representation to find spectral periodicities.

Unfortunately, `fft.py` has a known bug: it crashes (returns HTTP 500) when given a "near-singular" input—a sequence of all identical bases (e.g., "AAAAAAAAA") because the variance is zero. We cannot modify `fft.py` at this time.

Your task is to write a Bash script at `/home/user/gateway.sh` that acts as a reverse proxy and regression testing gateway. 
It must:
1. Start the two backend Python services (`python3 /app/aligner.py &` and `python3 /app/fft.py &`).
2. Bring up an HTTP server listening on port **8080** (you can use `socat` or `nc` in a loop).
3. Handle `POST /analyze` requests. The request body will contain a plain text DNA sequence.
4. For each request, the gateway should use `curl` to query both backend services:
   - `POST http://127.0.0.1:5000/align` with the sequence.
   - `POST http://127.0.0.1:5001/spectrum` with the sequence.
5. If `fft.py` fails (HTTP 500), your gateway must catch this and return the HTTP 200 response: `{"error": "near-singular sequence detected", "alignment": <alignment_result>}`.
6. If both succeed, combine the output and return HTTP 200: `{"alignment": <alignment_result>, "spectrum": <fft_result>}`.

Make sure your script remains running and listening on port 8080. Our automated test suite will send HTTP requests to `http://127.0.0.1:8080/analyze` to verify your implementation.