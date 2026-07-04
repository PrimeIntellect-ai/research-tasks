You are an AI assistant helping a developer organize and search old project files. 

The developer left an audio voice note about the archive's encryption key. 
1. First, process the audio file located at `/app/voicemail.wav` to determine the secret keyword (a single lowercase english word). You may use the provided `whisper` CLI tool (or any standard audio transcription utility available in the environment) to extract the text.
2. In the directory `/app/archive/`, there are several files ending in `.zdat`. These files use a custom "compression" which is simply a byte-wise XOR cipher applied to a CSV string. The XOR key is the secret keyword from the audio file (repeating the keyword as needed to match the string length).
3. We need a fast way to search the metadata of these files. Write a C program at `/home/user/search_server.c` and compile it to `/home/user/search_server`.
4. Your C program must act as a simple TCP server listening on `127.0.0.1:8050`.
5. When a client connects and sends a plain text query string terminated by a newline (e.g., `backup_2022\n`), the C program must:
   - Scan the `/app/archive/` directory for all `.zdat` files.
   - Read and decode the first 128 bytes of each file using the XOR secret keyword.
   - Parse the decoded content as comma-separated values (CSV). The first value in the CSV is the `project_name`.
   - If the `project_name` exactly matches the queried string, respond over the TCP socket with `MATCH: <filename>\n` (where `<filename>` is the base name of the file, e.g., `MATCH: file3.zdat\n`).
   - If no files match, respond with `NONE\n`.
   - Close the connection after responding.

Run your C program in the background so it remains active. Our automated system will test your server by connecting to `127.0.0.1:8050` and issuing test queries via TCP.