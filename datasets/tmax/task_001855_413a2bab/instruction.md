You are a bioinformatics analyst working with a legacy system. You have been given an audio file, a database of DNA sequences, and a C source file for sequence alignment. 

Your workflow consists of the following steps:

1. **Audio Decoding (Signal Processing):** 
   Analyze the audio file located at `/app/sequence_signal.wav`. This file contains a sequence of standard DTMF (Dual-Tone Multi-Frequency) tones. Decode the sequence of digits present in the audio. This sequence of digits forms the `REFERENCE_ID`.

2. **Reference Dataset Comparison:**
   Search the provided FASTA database at `/app/database.fasta` for the sequence whose header matches `>seq_[REFERENCE_ID]` (e.g., if the tones decode to 1234, look for `>seq_1234`). Extract this DNA sequence.

3. **Software Compilation and Analytical Validation:**
   You are provided with a C program at `/app/aligner.c` that calculates the local alignment score between two sequences. Compile this C program into an executable named `/app/aligner`. Ensure you link the math library.
   Run the compiled executable to compare your extracted reference sequence against all sequences in the file `/app/queries.fasta`. Identify the query sequence header that yields the highest alignment score against the reference sequence.

4. **Result Serving (Multi-Protocol):**
   Bring up an HTTP server listening exactly on `127.0.0.1:9090`.
   The server must respond to `GET /result` requests.
   It must require an HTTP header `Authorization: Bearer [REFERENCE_ID]` (using the decoded DTMF digits).
   If the authorization is correct, it should return a 200 OK status with a plain text body exactly matching: `<winning_query_header>:<highest_score>` (e.g., `query_8:42`).
   If the authorization is missing or incorrect, it must return a 401 Unauthorized status.

Ensure the HTTP server remains running in the background so it can be automatically verified.