You are a storage administrator tasked with reclaiming disk space on a specialized logging server. A legacy application dumped thousands of uncompressed telemetry binary files into the `/app/telemetry_data/` directory. 

We no longer have the source code or documentation for the binary format, but we managed to find a screenshot of the legacy system's schema definition document at `/app/schema.png`. 

Your objective is to write a highly optimized Python script at `/home/user/compact_telemetry.py` that processes this dataset and shrinks it.

Here are the requirements for your script:
1. **Schema Extraction:** Read the schema definition from `/app/schema.png` (using OCR tools like `tesseract`) to understand the byte layout of the records. Each file consists of a continuous stream of these fixed-size records.
2. **Data Filtering & Compaction:** For every file in `/app/telemetry_data/`:
   - Read the file using memory-mapped I/O (`mmap`) for maximum throughput.
   - Iterate through the records. You must DISCARD the "PADDING" field entirely to save space.
   - You must ALSO discard any record where the `STATUS_CODE` (extracted based on the schema) is equal to `404` or `500`.
3. **Concurrent Processing & Locking:** Because there are many large files, your script must use Python's `multiprocessing` to process multiple files in parallel. The filtered records `(TIMESTAMP, SENSOR_ID, VALUE, STATUS_CODE)` must be appended to a single shared output binary file located at `/home/user/compacted_telemetry.bin`. You must use file locking (e.g., `fcntl.flock`) to prevent race conditions when the concurrent workers append their data to the shared output file.
4. **Output Format:** The output file `/home/user/compacted_telemetry.bin` must be a tightly packed binary file containing only the valid records, sequentially appended.

Write and execute your script. Your final output will be evaluated automatically. An automated verifier will read your `/home/user/compacted_telemetry.bin` file, compute the Mean Squared Error (MSE) of the recovered floating-point `VALUE`s against our hidden ground truth, and check that the MSE is strictly below a given threshold.