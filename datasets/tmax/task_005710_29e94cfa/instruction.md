You are acting as an automated artifact manager for a binary repository. Periodically, large metadata logs are uploaded alongside binary artifacts. These logs are compressed using gzip to save space. However, due to a misconfiguration in the legacy build nodes, the uncompressed text inside these gzip files is written in various character encodings, not just UTF-8.

Your task is to write and execute a Bash script at `/home/user/process_artifacts.sh` that will stream, normalize, and filter these logs without ever writing uncompressed data to disk (as the real logs are extremely large).

In the directory `/home/user/artifacts/`, you will find:
1. Several gzip-compressed log files (`*.log.gz`).
2. A manifest file named `encoding_manifest.csv`. This file contains comma-separated values mapping the filename to its internal character encoding (e.g., `build_node_1.log.gz,UTF-16LE`).

Your script must:
1. Read `encoding_manifest.csv`.
2. For each file listed, stream its decompressed contents.
3. Convert the character encoding from the specified original encoding to `UTF-8` on the fly.
4. Filter the stream to keep ONLY lines containing the exact string `[STATE: CORRUPTED]`.
5. Compress the resulting filtered UTF-8 stream on the fly and append it to a single master file located at `/home/user/corrupted_report.txt.gz`.

Constraints:
- You must use bash pipelines to handle the streaming, conversion, filtering, and compression (e.g., using `zcat`, `iconv`, `grep`, and `gzip`).
- Do not create any intermediate uncompressed files on the disk.
- Run the script so that `/home/user/corrupted_report.txt.gz` is successfully generated before you finish.