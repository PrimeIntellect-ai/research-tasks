You are an AI assistant acting as an artifact manager for a local binary repository. 

Your objective is to extract and analyze a specific artifact that has been split, custom-compressed, and stored in a repository located at `/home/user/artifact_repo`.

Here are your instructions:
1. Navigate to `/home/user/artifact_repo`.
2. Read the `manifest.json` file. Find the artifact with the `id` equal to `"model_weights_v2"`.
3. The manifest lists the filenames of the chunks that make up this artifact in the correct sequential order.
4. Merge these chunks to reconstruct the compressed artifact.
5. The combined binary data has been obfuscated and compressed. To decode it, you must perform the following custom decompression pipeline:
   - First, apply a byte-wise XOR operation using the key `0x42` on every byte of the combined data.
   - Second, decompress the resulting bytes using standard `zlib` decompression.
6. The fully decompressed data represents a sequence of standard IEEE 754 32-bit little-endian floating-point numbers (`float` in C / `<f` in Python's struct).
7. Write a Python script to save the decompressed binary data to a temporary file, and then use Python's `mmap` module (memory-mapped I/O) to read through the binary file and find the maximum floating-point value in the sequence.
8. Save this maximum value to a file at `/home/user/result.txt`, formatted to exactly 4 decimal places (e.g., `123.4567`). Do not include any other text in the file.

All operations should be performed within `/home/user`. Write and execute Python scripts to accomplish this.