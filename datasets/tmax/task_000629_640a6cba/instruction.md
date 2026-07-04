You are tasked with building a parser for a legacy configuration management system that tracks state changes using a custom binary snapshot format. 

You have been provided with a snapshot file at `/home/user/config_snapshot.dat`.

Your goal is to write a C program that reads this custom binary file, decompresses the payload, extracts specific configuration sections, converts them into JSON, and generates a manifest file containing a checksum and metadata.

**Snapshot File Format (`config_snapshot.dat`):**
The file is a binary archive containing a custom 16-byte header followed by a GZIP compressed payload. All integer fields in the header are 32-bit unsigned integers in little-endian byte order.
- Bytes 0-3: Magic number `0x43464753` (ASCII 'CFGS')
- Bytes 4-7: Unix timestamp of the snapshot creation
- Bytes 8-11: Compressed payload size (bytes)
- Bytes 12-15: Uncompressed payload size (bytes)
- Bytes 16+: GZIP compressed payload.

**Uncompressed Payload:**
The decompressed payload is a plain text file containing configuration keys in an INI-like format. For example:
```
[General]
Key1=Value1
[Network]
Key2=Value2
```

**Your Objective:**
1. Write a C program at `/home/user/parser.c` and compile it (you may use `zlib` for decompression, and you have `sudo` privileges to install `zlib1g-dev` and `jq` if needed).
2. The C program must parse `/home/user/config_snapshot.dat`.
3. Extract ONLY the configuration key-value pairs under the `[Network]` and `[Security]` sections. Ignore all other sections.
4. Convert the extracted configurations into a strictly formatted JSON file at `/home/user/parsed_config.json`. 
   The JSON must have the sections as top-level objects, and their keys as string values. E.g.:
   ```json
   {
     "Network": {
       "IPAddress": "192.168.1.100",
       "Port": "8080"
     },
     "Security": {
       "EnableSSL": "true"
     }
   }
   ```
   *(Ensure standard formatting. You may use external shell tools or C libraries to format the JSON cleanly, as long as it's structurally identical.)*
5. Generate a manifest file at `/home/user/manifest.txt` with exactly the following format (including the newline):
   ```
   TIMESTAMP=<Extracted Unix Timestamp from Header>
   SHA256=<SHA256 checksum of /home/user/parsed_config.json>
   ```

You must execute your compiled program and ensure `/home/user/parsed_config.json` and `/home/user/manifest.txt` are created successfully.