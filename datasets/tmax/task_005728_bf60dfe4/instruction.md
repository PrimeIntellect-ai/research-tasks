You are a developer tasked with organizing a messy directory of project files containing dynamic shared objects (compiled libraries) and routing configurations. 

You need to write a pure Bash script at `/home/user/organizer.sh` that automates this cleanup. Currently, there is a rudimentary Python script `/home/user/legacy_parser.py` that partially parses the route definitions, but it cannot handle the shared library Application Binary Interface (ABI) checks or checksum validations. Your task is to implement the full logic entirely in Bash.

Here are your requirements:
1. **URL Routing and Parameter Parsing:**
   Read the file `/home/user/project_files/routes.conf`. Each line has the format:
   `ROUTE <url_path>[?<query_params>] => <library_name> : <expected_md5>`
   *Example:* `ROUTE /api/v1/auth?token=str => libauth.so : 9a3b...`
   Your Bash script must parse each line, extracting the `<url_path>` (ignoring the `?` and any `<query_params>`), the `<library_name>`, and the `<expected_md5>`.

2. **Checksum and Integrity Validation:**
   For each parsed route, locate the corresponding shared library in `/home/user/project_files/libs/`. 
   Verify that the MD5 checksum of the file exactly matches the `<expected_md5>` from the config file. If the file does not exist or the checksum fails, skip this route and print "CHECKSUM FAILED: <library_name>".

3. **Shared Library ABI Management:**
   If the checksum is valid, you must verify the library's ABI. Use the `nm` tool to check if the shared library exports the symbol `route_handler` in the text (T) section. 
   If the symbol is missing, skip the route and print "ABI FAILED: <library_name>".

4. **File Organization:**
   If a library passes both the checksum and ABI checks, organize it:
   Create a directory structure under `/home/user/organized_routes/` that mirrors the `<url_path>` (without the leading slash). 
   *Example:* For `/api/v1/auth`, create `/home/user/organized_routes/api/v1/auth/`.
   Copy the valid library into this new directory.
   Finally, write the word `VALID` to a file named `status.txt` in that same directory.

Run your `/home/user/organizer.sh` script once you have written it to perform the actual organization. Make sure your script is executable.

The final system state will be evaluated based on the correct creation and placement of the shared libraries and `status.txt` files in `/home/user/organized_routes/`.