You are a data engineer maintaining a legacy ETL pipeline. The pipeline extracts raw data from an older system and processes it using a proprietary, high-performance tool located at `/app/chunk_reader`. 

Recently, the ETL pipeline has been halting because certain exported data chunks are corrupted and cause the `/app/chunk_reader` tool to crash. We need to implement a pre-filtering step to quarantine these corrupted chunks before they reach the reader.

We have collected a small sample of chunks:
- `/home/user/samples/clean/` contains chunks that are successfully processed.
- `/home/user/samples/evil/` contains corrupted chunks that cause `/app/chunk_reader` to crash.

Your task is to:
1. Reverse engineer the binary data model of these chunks by analyzing the `/app/chunk_reader` binary and the provided samples.
2. Identify the structural flaw or index anomaly that triggers the crash in the legacy reader.
3. Write a Python script at `/home/user/chunk_filter.py` that acts as a sanitiser.

The script must accept a single command-line argument (the path to a chunk file).
- If the chunk is structurally sound and safe for the reader, the script must exit with code `0`.
- If the chunk contains the anomaly that would crash the reader, the script must exit with code `1`.

Your solution will be evaluated against a hidden, much larger corpus of clean and evil chunks. To pass, your script must correctly classify 100% of the clean chunks (exit 0) and 100% of the corrupted chunks (exit 1).