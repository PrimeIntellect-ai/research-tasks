You are an automated artifact manager curating a binary repository. Your task is to process a large incoming directory of mixed files, extract only the valid Linux executables (ELF files), chunk them for distributed storage, and generate a secure manifest, finally serving the repository over HTTP.

The incoming files are located in `/home/user/incoming_artifacts`. They have random names and extensions. Some are text files, some are Windows PE files, and some are ELF binaries. 

Your requirements are as follows:

1. **Identify ELF Binaries:** Write a Python script, `/home/user/curator.py`, that recursively searches through `/home/user/incoming_artifacts`. It must identify files as ELF binaries strictly by reading the first 4 bytes of the file (the "magic bytes" must be `\x7FELF`). Ignore file extensions entirely.
2. **Chunking:** For every ELF binary found, split the file into exact 512 KB (524,288 bytes) chunks (the final chunk may be smaller). Store these chunks in the directory `/home/user/repo/chunks/`. The chunks must be named using the pattern: `<original_file_sha256>_chunk_<index>`, where `<index>` is a 4-digit zero-padded integer starting at `0000`.
3. **Manifest Generation:** Your script must generate a JSON manifest at `/home/user/repo/manifest.json`. The JSON must strictly follow this structure:
    ```json
    {
      "artifacts": [
        {
          "original_name": "exact_filename_without_path",
          "original_sha256": "sha256_hex_digest_of_entire_original_file",
          "chunks": [
            {
              "chunk_name": "<original_sha256>_chunk_0000",
              "chunk_sha256": "sha256_hex_digest_of_this_chunk"
            },
            ...
          ]
        },
        ...
      ]
    }
    ```
4. **Logging:** Redirect the standard output and standard error of your `curator.py` script to `/home/user/repo/curation.log`.
5. **Serving:** Once the manifest and chunks are generated, start a Python-based HTTP server in the background that serves the `/home/user/repo` directory on `0.0.0.0` port `8080`. Save the process ID (PID) of this server to `/home/user/repo/server.pid`. Ensure the server stays running.

Ensure all dependencies and directories are correctly set up before running your script.