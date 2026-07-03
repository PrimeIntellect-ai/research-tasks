You are a deployment engineer tasked with rolling out a secure update receiver mechanism for our embedded filesystem devices.

Your objectives:
1. **Audio Analysis:** We received an automated voicemail from the network architect containing the assigned port for the new secure update server. The audio file is located at `/app/voicemail.wav`. Transcribe or listen to this file to extract the correct port number. 
2. **Web Server Setup (TLS):** Create a secure, unprivileged web server listening on the port mentioned in the audio file. 
    * The server must use HTTPS. Generate a self-signed TLS certificate and key, placing them in `/home/user/certs/server.crt` and `/home/user/certs/server.key`.
    * You may use any user-space tool available (e.g., Python's `http.server` with `ssl` wrapping) since you do not have root access.
    * The server should serve a file at `/home/user/www/index.html` containing exactly the string: `Deployment Node Active`.
3. **Connectivity & CI/CD Security Filter:** Our CI/CD pipeline extracts update archives to the filesystem, but it is currently vulnerable to directory traversal and shell injection attacks via malicious filenames. 
    * Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
    * The program must read a single filename string from `stdin` (up to 256 characters) until EOF or newline.
    * It must return an exit code of `0` (Safe) if the filename contains ONLY alphanumeric characters, dots (`.`), dashes (`-`), and underscores (`_`).
    * It must return an exit code of `1` (Malicious/Invalid) if the filename contains any other characters (e.g., slashes `/`, null bytes, shell operators, spaces, directory traversal dots like `..`, etc.). Note that `..` is explicitly forbidden even though `.` is allowed.
4. **Adversarial Verification:** We have provided test corpora for your C program.
    * Clean filenames: `/app/corpora/clean/`
    * Evil filenames: `/app/corpora/evil/`
    * Your compiled `/home/user/sanitizer` must be tested against every file in these directories (e.g., `/home/user/sanitizer < /app/corpora/clean/test1.txt`). 
    * Ensure your program successfully accepts 100% of the clean corpus (exit code 0) and rejects 100% of the evil corpus (exit code 1).

Complete the setup, leave your TLS server running in the background, and ensure your compiled `sanitizer` binary is in `/home/user/`.