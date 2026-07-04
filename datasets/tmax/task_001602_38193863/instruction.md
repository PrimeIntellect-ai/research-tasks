You are tasked with fixing and securing a performance bottleneck in our spectroscopy processing pipeline. 

We have a data processing system that performs curve fitting and Monte Carlo simulations on incoming spectroscopy data to resolve overlapping peaks. The system consists of three services:
1. A Redis message queue.
2. A Python Flask API frontend.
3. A C-based backend worker that pulls jobs from Redis and performs matrix operations.

Currently, the C backend experiences severe performance degradation (hanging or crashing) when processing "near-singular" inputs—specifically, spectral data with highly collinear or perfectly flat regions. 

Your objectives are two-fold:

**Phase 1: Multi-Service Configuration**
The startup script `/app/start.sh` and the configuration files in `/app/config/` are currently misconfigured. The Flask app (port 5000) cannot talk to Redis (port 6379), and the worker is pointing to the wrong socket. 
1. Modify `/app/start.sh` and the configs so that the end-to-end flow works. The services must start properly.
2. An end-to-end test will send a POST request to `http://localhost:5000/process` with a valid JSON payload, and the C worker must successfully process it and write the result to Redis.

**Phase 2: Adversarial Input Filter (Sanitiser)**
To protect the backend from near-singular inputs, write a C program located at `/app/src/filter.c` (which compiles to `/app/bin/filter`). 
This filter must:
1. Accept a single command-line argument: the path to a CSV file containing spectroscopy data (two columns: wavelength, intensity).
2. Analyze the input to determine if it is "clean" (safe to process) or "evil" (near-singular, highly collinear, or flat, which would crash the backend).
3. Exit with status code `0` if the file is clean and should be preserved/accepted.
4. Exit with status code `1` if the file is evil and should be rejected.

We have provided sample datasets in `/app/corpus/clean/` and `/app/corpus/evil/` to help you tune your filter. Your `filter` binary will be tested against a hidden evaluation corpus of clean and evil files.

Compile your filter with: `gcc -O3 /app/src/filter.c -o /app/bin/filter -lm`

Ensure all services are running and your filter executable is placed exactly at `/app/bin/filter` when you are finished.