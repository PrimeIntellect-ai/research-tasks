You have inherited a legacy data ingestion pipeline from a previous developer. The pipeline is located at `/home/user/pipeline/` and consists of a Bash script `ingest.sh` that processes a directory of encoded data files located in `/home/user/pipeline/data/`.

Currently, the pipeline has two major bugs:
1. **Encoding/Decoding Failure**: When running `/home/user/pipeline/ingest.sh`, it crashes halfway through processing the files due to one specific file being encoded with a different algorithm (not base64 like the rest). 
2. **Intermediate State Leak**: Even if you bypass the bad file, the generated `/home/user/pipeline/out/summary.txt` file is incorrect. It flags way too many files as `CRITICAL`. There is a state tracing issue in the Bash script where variables are leaking between loop iterations.

Your task:
1. Use delta debugging or tracing techniques to identify the single file in `/home/user/pipeline/data/` that is causing the decoding failure.
2. Move this problematic file to `/home/user/pipeline/quarantine/` (keep its original filename).
3. Debug and modify `/home/user/pipeline/ingest.sh` to fix the state leakage so that only files that actually decode to `STATUS: CRITICAL` are written to the summary file.
4. Run the fixed `/home/user/pipeline/ingest.sh` to generate the correct `/home/user/pipeline/out/summary.txt`.

Ensure your final run of the script exits with code 0 and produces the exact correct summary.