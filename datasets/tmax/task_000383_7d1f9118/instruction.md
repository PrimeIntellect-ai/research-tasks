You are an AI assistant helping a technical writer organize a scattered, legacy documentation dump. The writer has left you a set of multi-part nested archives, an audio memo with critical deployment instructions, and a request to normalize all documentation and serve it dynamically.

Here are the details of your tasks:

1. **Extract the Nested Archive:**
   You will find a multi-part archive starting at `/app/legacy_docs.tar.gz.001` (along with `.002`, etc.). Combine and extract these files. Inside, you will find another archive, `internal_files.zip`. Extract this as well into `/home/user/extracted_docs/`.

2. **Normalize Encodings and Apply Macros:**
   The extracted text files inside `/home/user/extracted_docs/` are in various character encodings (e.g., UTF-16LE, ISO-8859-1).
   - Write a Bash script to recursively detect the encoding of each `.txt` file and convert it to UTF-8 using standard CLI tools like `iconv` or `file`.
   - Using standard text processing tools (like `sed` or `awk`), apply a macro to all converted files: replace any instance of `[[TITLE:(.*?)]]` with `<h1>\1</h1>` and `[[BOLD:(.*?)]]` with `<strong>\1</strong>`. 
   - Overwrite the original files with these UTF-8, HTML-tagged versions.

3. **Audio Transcription & Integration:**
   The technical writer left an audio memo at `/app/writer_notes.wav`. Transcribe this audio file using any standard CLI tool or API accessible from the terminal (e.g., `ffmpeg` paired with a transcription script, or `whisper` if you can install it). 
   The audio contains three critical pieces of information:
   - A secret **Authorization Token**.
   - A specific **Port Number**.
   - A **Sign-off phrase**.
   
   You must append the extracted Sign-off phrase as a new line at the very end of every normalized `.txt` file.

4. **Serve the Documentation:**
   Write a Bash-only server (using `socat` or `nc`) that listens on the localhost IP (`127.0.0.1`) and the Port Number specified in the audio memo. 
   - The server must implement a basic HTTP GET protocol.
   - It must verify the `Authorization: Bearer <TOKEN>` header matches the token from the audio. If unauthorized, return `HTTP/1.1 401 Unauthorized`.
   - If authorized, and the client requests a file (e.g., `GET /chapter1.txt HTTP/1.1`), the server must return `HTTP/1.1 200 OK` followed by the exact contents of that file from the `/home/user/extracted_docs/` directory.

Write all your scripts in standard Bash. Keep the server running in the background when you are finished so it can be verified.