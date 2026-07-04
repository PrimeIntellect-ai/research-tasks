You are a storage administrator managing a Linux server that is running out of disk space. You have identified that a proprietary backup system is leaving behind large, monolithic archive files ending in `.blob`. These files contain concatenated data chunks, many of which are obsolete, but the backup system itself is broken and cannot compact them.

Your task is to reclaim disk space by finding these files, parsing their binary structure, filtering out old data, and merging the valid data into new compacted files.

Here is the specification of what you need to do:

1. **Find Target Files**: Search the directory tree starting at `/home/user/storage_pool` for all files ending with the `.blob` extension that are strictly larger than 1 Megabyte (1,048,576 bytes).

2. **Understand the Binary Format**: Every `.blob` file is a sequence of chunks. Each chunk consists of a 32-byte header followed immediately by the payload data.
   The 32-byte header has the following format (all integers are Little-Endian):
   - Bytes 0-3: Magic sequence `BLOB` (ASCII)
   - Bytes 4-11: Unix timestamp (64-bit unsigned integer)
   - Bytes 12-15: Payload size `N` in bytes (32-bit unsigned integer)
   - Bytes 16-31: Original filename (ASCII string, padded with null bytes `\x00`)
   Immediately after the 32-byte header, there are exactly `N` bytes of payload data. The next chunk (if any) starts immediately after this payload.

3. **Filter and Compact**: Write a Python script `/home/user/compact_blobs.py` that takes an input `.blob` file path and an output `.blob` file path. It should parse the input file, extract the headers, and write ONLY the chunks whose timestamp is strictly greater than `1700000000` to the output file. The chunks written to the output file must be in the same order and perfectly preserve the original 32-byte header and payload.

4. **Execute**: Create a directory `/home/user/compacted_pool`. Use your script (and standard bash commands) to process every target file you found in step 1. Save the compacted versions in `/home/user/compacted_pool/` using the exact same base filename (e.g., if the original was `/home/user/storage_pool/backups/data1.blob`, the new file should be `/home/user/compacted_pool/data1.blob`).

5. **Report**: Create a file named `/home/user/reclaimed_space.txt`. It must contain exactly one line with two integers separated by a single space: `[Total Original Bytes] [Total Compacted Bytes]`. 
   - `[Total Original Bytes]` is the sum of the file sizes of all the original target `.blob` files you processed.
   - `[Total Compacted Bytes]` is the sum of the file sizes of all the newly created compacted `.blob` files.

Ensure your code handles the binary data correctly and does not load excessively large payloads into memory at once if it can be avoided (chunk-based streaming).