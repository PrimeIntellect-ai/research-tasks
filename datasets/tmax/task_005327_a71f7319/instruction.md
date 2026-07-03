You are managing a local binary artifact curation pipeline for our internal development team. The system is composed of three cooperating services:
1. An Upload Gateway (Flask application running on `127.0.0.1:5000`).
2. A Metadata Cache (Redis running on `127.0.0.1:6379`).
3. A Storage Backend (A simple HTTP file server running on `127.0.0.1:8000`).

Currently, the Upload Gateway accepts any uploaded file and forwards it to the Storage Backend. We recently suffered outages because developers uploaded malformed or malicious custom-compressed artifacts. 

The artifacts use a proprietary binary format called "C-ZIP". The format specification is:
- **Magic Bytes:** 4 bytes, ASCII `CZIP`
- **Uncompressed Size:** 4 bytes, unsigned integer, little-endian
- **Filename Length:** 2 bytes, unsigned integer, little-endian
- **Filename:** Variable length ASCII string (length determined by the previous field)
- **Payload:** The remaining bytes are zlib-compressed data.

Your task is to write a Python script, `/home/user/app/artifact_filter.py`, that acts as a mandatory pre-processor and sanitizer. It must expose a CLI invocation: `python3 /home/user/app/artifact_filter.py <input_file_path> <output_dir>`.

Requirements for `/home/user/app/artifact_filter.py`:
1. Parse the C-ZIP binary file.
2. Reject (exit with code 1) any file that:
   - Does not start with the correct `CZIP` magic bytes.
   - Contains path traversal sequences (e.g., `../`, `/`, or `..\\`) in the parsed filename.
   - Is a decompression bomb: specifically, if the declared Uncompressed Size is greater than 10,000,000 bytes (10MB).
3. If the file is valid (clean), it must be accepted. The script should bulk-rename the file to its SHA256 hash (e.g., `<sha256_of_original_file>.czip`) and copy it to `<output_dir>`. It must then exit with code 0.

To test your filter, we have provided two corpora of artifacts in `/home/user/corpora/`:
- `/home/user/corpora/clean/`: Contains valid C-ZIP artifacts.
- `/home/user/corpora/evil/`: Contains malicious or malformed artifacts (path traversals, wrong magic bytes, decompression bombs).

Additionally, you must reconfigure the Upload Gateway located at `/home/user/app/gateway.py`. Modify it so that upon receiving a file, it first saves it to a temporary directory, runs your `artifact_filter.py` against it with `/home/user/app/staging/` as the output directory, and only if the script returns exit code 0, forwards the renamed SHA256 file from staging to the Storage Backend.

Start the services by running `bash /home/user/app/start_services.sh`. Ensure all services are running and your `artifact_filter.py` correctly sanitizes the corpora. Write a log file to `/home/user/app/filter_results.log` detailing which files were accepted and rejected during your local testing.