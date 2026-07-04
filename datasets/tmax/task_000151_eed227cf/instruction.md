You are a data engineer tasked with building a robust, multi-stage ETL pipeline in a Linux environment. The pipeline must filter out malicious payloads from JSON-lines logs, perform a rolling aggregation, and output the normalized data. 

Your tasks are:

1. **Audio Transcription & Configuration Extraction**
   You have been provided with an audio artifact at `/app/config.wav`. This file contains a short spoken configuration parameter dictated by the lead architect. You must transcribe this audio to discover the integer "window size" required for the rolling aggregation step later.

2. **C-based JSON-Lines Sanitizer (Adversarial Filter)**
   You must write a C program named `/home/user/filter.c` and compile it to `/home/user/filter_bin`.
   - The program must read JSON-lines from standard input (`stdin`) and write valid, clean JSON-lines to standard output (`stdout`).
   - Standard error (`stderr`) can be used for logging.
   - You may use `jansson` (`libjansson-dev` is available) or write your own parser.
   - **The Vulnerability / Scenario Anchor:** Malicious actors are attempting to bypass simple text filters by encoding restricted keywords using Unicode escape sequences (e.g., `\u0045` for `E`). 
   - **Filtering Logic:** Your C program must fully decode string values in the JSON. If the top-level string field `"message"` contains the exact substring `EXFIL` (case-sensitive) *after* decoding all Unicode escapes, the entire JSON record must be **dropped** (rejected). If it does not contain `EXFIL`, it must be **preserved** (printed to stdout exactly as it came in, or re-serialized as valid JSON).
   - Your compiled program will be tested against two corpora:
     - `/app/corpus/clean/` (contains logs that MUST be accepted)
     - `/app/corpus/evil/` (contains obfuscated malicious logs that MUST be rejected)

3. **Rolling Aggregation & Multi-stage Pipeline**
   Write a shell script `/home/user/pipeline.sh` that:
   - Takes a file path as its first argument (e.g., `./pipeline.sh /app/corpus/clean/input.jsonl`).
   - Pipes the file contents through your C filter (`/home/user/filter_bin`).
   - Pipes the clean output into a tool of your choice (e.g., `awk`, `python3`, or additional C code) to compute a rolling moving average of the top-level `"bytes"` field.
   - The rolling average must use the window size you extracted from the `/app/config.wav` audio file. (If the window size is $W$, the output at line $N$ is the average of the `"bytes"` values from line $N-W+1$ to $N$). For the first $W-1$ lines, the average should be computed over the available lines.
   - Output the final result as a CSV file to standard output, with the columns `timestamp,bytes,rolling_avg_bytes`.

Ensure your C program is robust against deeply nested JSON or malformed Unicode escapes (if an escape is malformed, you may either drop the record or treat the escape safely, but you must not crash).