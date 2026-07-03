You are an artifact manager responsible for curating binary repositories. We have recently received a massive influx of artifact uploads. These artifacts are stored as split chunks to bypass file size limits, but we suspect a threat actor has been injecting corrupted or malicious payloads into the repository.

Your task is to write a fast, reliable artifact classifier script at `/home/user/artifact_filter.sh`. 

Whenever an artifact is uploaded, it is stored in its own directory as a series of sequential chunks (e.g., `chunk_aa`, `chunk_ab`, `chunk_ac`). When concatenated in alphabetical order, these chunks form a `gzip`-compressed `tar` archive.

A legacy scanner binary is located at `/app/legacy_scanner`. It is a stripped ELF binary that historically checked uncompressed text files for a specific, proprietary malicious watermark. However, the binary is too slow to run on every file in our new scale, and it cannot process split chunks, compressed streams, or archives.

Your script `/home/user/artifact_filter.sh` must take a single argument: the path to an artifact directory containing the split chunks. 
It must perform the following pipeline:
1. Merge the chunks in the correct alphabetical order.
2. Verify the structural integrity of the compressed archive (rejecting any with corrupted compression headers, invalid checksums, or trailing garbage).
3. Extract the contents and inspect the files.
4. Detect the malicious watermark that the `/app/legacy_scanner` looks for, accounting for the fact that the threat actor sometimes obfuscates the watermark by changing the character encoding of the text files.
5. Print EXACTLY the word `CLEAN` to standard output if the artifact is perfectly intact and free of the watermark. Print EXACTLY the word `EVIL` if the artifact is corrupted, fails decompression/tar integrity checks, or contains the malicious watermark.

You are provided with a small dataset of known artifacts to test your script against:
- `/app/corpus/clean/` contains subdirectories of perfectly clean artifacts.
- `/app/corpus/evil/` contains subdirectories of corrupted or malicious artifacts.

You must reverse engineer or analyze `/app/legacy_scanner` to determine exactly what watermark it detects and how it handles character encodings. Ensure your script handles file splitting/merging, compressed stream processing, and character encoding conversion reliably. 

Make sure `/home/user/artifact_filter.sh` is executable. The automated pipeline will invoke it as `/home/user/artifact_filter.sh /path/to/artifact/dir` for each artifact in a much larger, hidden dataset.