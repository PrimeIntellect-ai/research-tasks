You are an artifact manager responsible for curating legacy binary repositories. You have been given a set of unknown files in `/home/user/artifacts/` with the `.dat` extension. 

Your initial investigation reveals that these files are actually standard gzip-compressed files, despite lacking the `.gz` extension. When decompressed, each file contains a proprietary binary format.

The uncompressed binary format consists of:
1. A 16-byte header:
   - 4 bytes: ASCII magic string `BLOB`
   - 4 bytes: Unsigned 32-bit integer (little-endian) representing the Artifact ID
   - 8 bytes: Unsigned 64-bit integer (little-endian) representing a UNIX timestamp
2. A variable-length payload of arbitrary data following the header.

Your task is to write a Python script `/home/user/parser.py` and use shell commands to process these files. 

Requirements for `/home/user/parser.py`:
- It must accept exactly one command-line argument: the base filename of the artifact (e.g., `alpha.dat`).
- It must read the uncompressed binary data directly from standard input (`stdin`).
- It must extract the header, convert the UNIX timestamp to a UTC ISO8601 string formatted exactly as `YYYY-MM-DDTHH:MM:SSZ`.
- It must print a single valid JSON string to standard output representing the header metadata. The JSON keys must be exactly: `filename`, `id`, and `timestamp`. Example: `{"filename": "alpha.dat", "id": 42, "timestamp": "2020-01-01T00:00:00Z"}`.

Shell operations:
- Use standard stream redirection and pipes in your shell to decompress each `.dat` file in `/home/user/artifacts/` and pipe the uncompressed stream into your `/home/user/parser.py` script.
- Redirect and append the output of all these executions into a single file at `/home/user/manifest.jsonl`.
- Finally, sort the `manifest.jsonl` file alphabetically by line and save the result to `/home/user/manifest_sorted.jsonl`.