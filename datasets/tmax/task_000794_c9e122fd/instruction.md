You are a bioinformatics analyst tasked with reconstructing a sequence from a set of simulated reads, calibrating it against a visual barcode, and exposing your findings via a web service. 

Your workflow requires processing a video artifact, assembling a sequence from raw read data using a graph algorithm, estimating an error parameter via MCMC, and writing a C++ HTTP server to serve the results. 

**Step 1: Visual Barcode Extraction (Video Processing)**
You are provided a video at `/app/calibration.mp4`. This video is exactly 12 frames long. Each frame is uniformly colored. The colors map to DNA nucleotides as follows:
- Pure Red (High R, Low G, Low B) -> 'A'
- Pure Green (Low R, High G, Low B) -> 'C'
- Pure Blue (Low R, Low G, High B) -> 'G'
- Yellow (High R, High G, Low B) -> 'T'
Use `ffmpeg` or any other tool to extract the sequence of 12 nucleotides. This is the "calibration barcode".

**Step 2: Sequence Assembly (Graph Algorithms & C++)**
You have a dataset of short DNA reads in a text file at `/app/reads.txt` (one read per line). 
Write a C++ program that builds a De Bruijn graph (using k-mer size k=4) from these reads to assemble the single, continuous consensus sequence. The graph will have an Eulerian path that spells out the assembled sequence. The assembled sequence will start with the exact 12-nucleotide calibration barcode you extracted in Step 1.

**Step 3: Error Rate Estimation (MCMC in C++)**
Assume each character in the short reads was generated from the true assembled sequence with an unknown error probability `p` (substitution to any of the other 3 bases). 
In your C++ program, implement a simple Metropolis-Hastings MCMC sampler to estimate the posterior mean of `p`.
- Prior: Uniform(0, 0.5)
- Likelihood: Binomial (each base in every read is either a match or mismatch to the true assembled sequence at its aligned position). Note: You can assume reads align perfectly starting at their exact matching k-mers in the consensus.
- Run at least 5,000 MCMC iterations.

**Step 4: HTTP Service (Integration)**
Implement a minimal C++ HTTP server (you may use raw sockets or a header-only library like `cpp-httplib` which you can download) that listens on `0.0.0.0:8080`.
The server must respond to the following HTTP GET requests:
1. `GET /barcode`
   - Response body: The 12-character barcode string (e.g., `ACGTACGTACGT`).
2. `GET /consensus`
   - Response body: The fully assembled sequence string.
3. `GET /error_rate`
   - Response body: The estimated error rate `p` as a float (e.g., `0.045`).

**Requirements:**
- Your HTTP server must remain running in the foreground or background so that we can verify the endpoints.
- You must write the graph assembly, MCMC, and web server logic primarily in C++.
- The final binary must be compiled and executed to bind to port 8080.