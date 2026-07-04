You are tasked with building a security component for our internal binary artifact repository. We receive large binaries that are uploaded as split, chunked, and compressed payloads. Before we merge and store these binaries, we must validate their accompanying metadata manifests.

Recently, our security team updated the artifact validation policy, but the only surviving copy of the new rules is a screenshot of the legacy wiki page, located at `/app/artifact_policy.png`. 

Your objectives are:
1. Extract the new validation rules from the image `/app/artifact_policy.png`. You may use OCR tools (like `tesseract`, which is preinstalled) to read the policy.
2. Write a C++ program `/home/user/validator.cpp` that implements these exact rules.
3. The program must take a single command-line argument: the path to a gzipped JSON manifest file (`.json.gz`).
4. The C++ program must decompress the stream, parse the structured JSON data, and validate it against the policy rules extracted from the image.
5. If the manifest satisfies ALL rules, the program must terminate with exit code `0` (accept). If it violates any rule, it must terminate with exit code `1` (reject).
6. Compile your program to an executable named `/home/user/validator`. You may use standard libraries and `libz` (`-lz`) for decompression, or a header-only JSON library if you download one. 

The manifests will have the following JSON structure (when decompressed):
```json
{
  "artifact_name": "backend_service",
  "author": "dev_team_alpha",
  "build_id": "bld_9921",
  "compression_format": "gzip",
  "total_uncompressed_bytes": 45000000,
  "chunks": [
    {"part": 1, "size": 15000000},
    {"part": 2, "size": 15000000},
    {"part": 3, "size": 15000000}
  ]
}
```

Make sure your C++ code is robust against missing fields if the policy requires them. Write and compile the code, and ensure it's ready at `/home/user/validator`. We will test it against a hidden corpus of clean and malicious manifests.