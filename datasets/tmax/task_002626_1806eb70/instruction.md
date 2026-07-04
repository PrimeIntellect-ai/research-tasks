You are a technical writer tasked with organizing and securing a new batch of documentation for a software project. You must prepare the files, create a differential backup, and expose them via a simple custom TCP service.

Perform the following steps using standard Bash utilities (coreutils, sed, tar, nc, etc.):

1. **Safe Archive Extraction**: 
   You have received an archive at `/app/docs_update.tar`. The system that generated this archive is known to have a path traversal vulnerability, and it may contain entries that attempt to overwrite files outside the intended extraction directory (a "Tar Slip" issue). 
   Carefully inspect the binary headers/contents of the archive. Extract *only* the files intended for the `docs/` directory into a new directory at `/home/user/docs_clean/`. Do not allow any files to be extracted outside of `/home/user/docs_clean/`.

2. **Large-Scale Text Editing**:
   The documentation is currently marked as a draft. Using Bash tools (e.g., `sed` or `awk`), recursively find all `.md` files in `/home/user/docs_clean/` and replace every occurrence of the exact string `DRAFT_STATUS: INCOMPLETE` with `DRAFT_STATUS: FINAL`. 

3. **Incremental Backup**:
   The directory `/home/user/docs_original/` contains the previous version of the documentation. Create an archive named `/home/user/patch.tar.gz` that contains *only* the files in `/home/user/docs_clean/` that differ in content from their counterparts in `/home/user/docs_original/`, or are entirely new. 

4. **Audio Transcription & Secret Extraction**:
   A developer has left an audio note at `/app/interview.wav`. Use the provided transcription tools on the system (e.g., `whisper` CLI) to transcribe the audio file. The audio contains a spoken 3-word secret project code. Note this code.

5. **Custom TCP Documentation Server**:
   Write a Bash script at `/home/user/serve.sh` and run it in the background. This script must use `nc` (Netcat) or `socat` to listen on **TCP port 8000** in a continuous loop.
   - When a client connects, the server must read exactly one line of text.
   - If the client sends `PROJECT_CODE: <the_3_word_secret>`, the server must respond with the exact string `ACCESS_GRANTED\n`, followed immediately by the full text content of `/home/user/docs_clean/index.md`, and then close the connection.
   - If the client sends anything else (or an incorrect code), the server must respond with exactly `ACCESS_DENIED\n` and close the connection.

Ensure your server is running and bound to port 8000 before finishing the task. Do not use external programming languages like Python or Node.js for the server; use Bash and standard CLI utilities.