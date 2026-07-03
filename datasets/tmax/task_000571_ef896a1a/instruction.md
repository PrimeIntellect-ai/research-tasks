We are profiling a legacy bioinformatics pipeline that is producing non-reproducible results due to floating-point reduction order issues in its signal processing module. We need you to reimplement the core extraction and serving logic in Go to ensure strict reproducibility and performance.

An audio file containing raw encoded spectroscopic data (representing synthesized biomolecular signals) has been provided at `/app/signal_data.wav`. The audio contains a sequence of time-domain signals. 

Your task:
1. Write a Go program to read `/app/signal_data.wav`. Extract the audio samples (assume 16-bit PCM, mono, 44100Hz).
2. Perform an FFT on non-overlapping windows of exactly 4410 samples (0.1 seconds per window) to extract the frequency spectrum. 
3. For each window, identify the single dominant frequency peak (the frequency bin with the highest magnitude).
4. Map each dominant frequency to a standard amino acid character (FASTA format) using the following mapping:
   - 1000 Hz (+/- 50 Hz): 'A'
   - 1500 Hz (+/- 50 Hz): 'C'
   - 2000 Hz (+/- 50 Hz): 'G'
   - 2500 Hz (+/- 50 Hz): 'T'
   - Ignore windows where the peak magnitude is negligible or falls outside these ranges.
5. Construct a standard FASTA string from the extracted sequence. Use the header `>Extracted_Sequence`.
6. Implement a Go-based HTTP and TCP server to serve this sequence. 
   - The HTTP server must listen on `127.0.0.1:8080`. When a `GET /sequence` request is made with the header `Authorization: Bearer bio-perf-token`, it should return the raw FASTA string with a `200 OK` status. Any other request or invalid token should return `401 Unauthorized` or `404 Not Found`.
   - The TCP server must listen on `127.0.0.1:9090`. When a client connects and sends the exact string `PING\n`, it should respond with the extracted FASTA string followed by `\n` and close the connection.

Ensure your Go application is running in the background and listening on both ports before completing your run. Save your Go source code at `/home/user/pipeline.go`.