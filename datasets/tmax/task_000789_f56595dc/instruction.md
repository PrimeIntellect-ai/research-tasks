You are a bioinformatics analyst working with an unconventional lab setup that transmits telemetry and sequence data via acoustic signals. 

We have received a sonified biological sequence in the file `/app/sequence_signal.wav`. The sequence was transmitted using standard DTMF (Dual-Tone Multi-Frequency) tones. The lab uses the following encoding for nucleotides:
- Tone '1' = A
- Tone '2' = C
- Tone '3' = G
- Tone '4' = T

Your task is to:
1. Decode the DTMF tones from the audio file to recover the DNA sequence (you may use `multimon-ng`, which is installed on the system).
2. Treat the sequence as a Markov chain and compute the empirical transition counts (posterior mode of the transition matrix assuming a uniform prior). You only need to count the overlapping pairs (e.g., the sequence "ACT" has transitions A->C and C->T).
3. Format the transition counts as a comma-separated list of `pair:count` in alphabetical order of the pair. Always include all 16 possible pairs (AA, AC, AG, AT, CA, ..., TT), even if the count is 0. Example format: `AA:0,AC:2,AG:0,AT:1,CA:0...`
4. Serve these formatted counts as a plain text response via an HTTP server listening on `127.0.0.1:9000`. You must implement this server using only Bash and standard utilities (like `nc` or `socat`). The server should run continuously, accept incoming HTTP GET requests, and respond with a valid `HTTP/1.1 200 OK` header followed by the exact transition counts string in the body.

Do not use Python or other high-level languages for the implementation; stick to Bash, coreutils, and standard CLI tools. Keep the server running in the background or foreground so that we can verify the output by querying the port.