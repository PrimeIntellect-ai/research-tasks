You are a DevOps engineer tasked with debugging a custom log parsing tool. The tool is written in Rust and is designed to extract message payloads from a production server log file. 

The previous engineer wrote a naive parsing function in `/home/user/log_parser/src/main.rs`. However, it has a couple of critical flaws:
1. It has an off-by-one boundary condition error: extracted payloads incorrectly include the opening `<` character.
2. It fails to correctly extract payloads that contain a `>` character within the message itself (a parsing edge-case).

Your task is to:
1. Diagnose and fix the parsing logic in `/home/user/log_parser/src/main.rs`. 
2. Build and run the repaired Rust program.
3. Redirect the standard output of the fixed program into a new file located at `/home/user/parsed_payloads.txt`.

The source log file is located at `/home/user/server.log`. The expected format of `/home/user/parsed_payloads.txt` is exactly one extracted payload per line, with no enclosing `< >` tags from the main log structure.

Do not modify the original `/home/user/server.log` file.