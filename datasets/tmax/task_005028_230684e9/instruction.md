You are an IT security and backup administrator. We have an old proprietary backup system that packages log files into a custom archive format (`.bkp`). 

We recently discovered that our legacy extraction tool (`/app/legacy_extractor`, provided to you as a stripped binary) is vulnerable to "Zip Slip" attacks—it blindly follows directory traversal characters (like `../`) in archived filenames, overwriting files outside the intended extraction directory.

Your task is to write a secure replacement in C that acts as a web service to safely receive, extract, and parse these archives. 

Specifically, you must write and run a C program that:
1. Listens for HTTP POST requests on `127.0.0.1:8080` at the endpoint `/upload`.
2. The POST request body will contain the raw bytes of a `.bkp` archive.
3. You must parse the archive format in your C code (do not use the legacy binary for extraction in your server, as it is unsafe. You can analyze `/app/legacy_extractor` using standard reverse-engineering tools like `strace`, `ltrace`, `strings`, or `xxd` on sample inputs to deduce the simple `.bkp` file format).
4. For each file in the archive, safely extract it into `/home/user/extracted/`. To prevent Zip Slip, you must strip all directory components from the archived filename and keep only the base filename (e.g., `../../etc/passwd` must be extracted as `/home/user/extracted/passwd`).
5. The extracted files are multi-line logs with the following strict format:
   ```
   === LOG START ===
   Date: YYYY-MM-DD
   Time: HH:MM:SS
   Event: <EventName>
   Details:
   <multi-line details, can be any length>
   === LOG END ===
   ```
6. After extracting a file, safely parse the multi-line log to extract the Date and Time. Bulk rename the extracted file in `/home/user/extracted/` to be prefixed with the timestamp: `YYYYMMDD_HHMMSS_<base_filename>`.
7. The HTTP response to the POST request must be `HTTP/1.1 200 OK` with a plaintext body containing exactly the `<EventName>` of the *first* file processed in the archive.

Requirements:
- C program should be compiled to `/home/user/server`.
- Run the server in the background so it is listening when we verify.
- Create the `/home/user/extracted/` directory.
- The binary `/app/legacy_extractor` is provided solely for you to reverse-engineer the `.bkp` format.

Write the code, compile it, and ensure the service is running on port 8080.