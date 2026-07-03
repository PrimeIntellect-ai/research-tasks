You are an artifact manager tasked with curating binary repositories for a secure system. You have received a transmission containing your configuration instructions and a sample artifact repository. 

Your task is to build a curation service in C that processes custom artifact bundles, extracts the underlying binaries, and identifies valid executables.

1. **Configuration Retrieval:**
   There is an audio file at `/app/transmission.wav`. You must transcribe this audio to discover your required configuration. The audio dictates:
   - The TCP port your service must listen on.
   - The security token required to authenticate requests.

2. **Artifact Format & Processing:**
   Your service will be tested against artifact files (e.g., `/home/user/test_artifact.artf`). The `.artf` format is a custom binary wrapper:
   - Bytes 0-3: Magic header `ARTF`
   - Bytes 4-7: 32-bit unsigned integer (little-endian) representing the payload size `N`.
   - Bytes 8 to 8+N-1: A nested archive payload (specifically, a `.tar.gz` file).

   Your C service must:
   - Read the `.artf` file and validate the `ARTF` magic header.
   - Extract the inner `.tar.gz` payload and save it to disk.
   - Decompress and extract the tarball. The tarball may contain sub-directories, other archives (like `.zip`), text files, and binary files. You must extract everything to `/home/user/extracted_artifacts/`.
   - Scan all extracted files to identify valid ELF executables. A file is a valid ELF if its first 4 bytes match the ELF magic number (`\x7F ELF`).

3. **Service Interface:**
   Write your service in C (save the source as `/home/user/artifact_server.c` and compile it to `/home/user/artifact_server`). 
   The service must be a simple HTTP server (you may use raw sockets, `libmicrohttpd`, or any other C library available in the environment).
   
   It must expose the following endpoint:
   `GET /curate?artifact=<path_to_artf>&token=<security_token>`
   
   - If the token does not match the secret from the audio, return `HTTP 401 Unauthorized`.
   - If the file cannot be read or the `ARTF` magic is missing, return `HTTP 400 Bad Request`.
   - Upon success, extract the archive, find the ELF files, and return an `HTTP 200 OK` with a JSON array of the base filenames of all valid ELF files found, e.g., `["program1", "util_tool"]`.

Ensure your C server is running in the background before you finish the task. You are free to install any tools (like `ffmpeg`, `whisper-cpp`, or `libmicrohttpd-dev`) needed to accomplish this.