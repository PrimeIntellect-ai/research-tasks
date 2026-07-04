You are tasked with completing a partial migration from Python 2 to Python 3 for a request routing component, and creating a Bash-based processing pipeline that incorporates memory profiling and rate limiting.

Currently, we have a Python 2 script `/home/user/legacy_parser.py` that parses a URL, extracts its domain, and serializes this data into a protobuf message.

Here is what you need to do:

1. **Protobuf Setup**:
   - Compile `/home/user/request.proto` into Python bindings in `/home/user/` using `protoc`. 
   
2. **Python 2 to 3 Migration**:
   - Update `/home/user/legacy_parser.py` to be fully Python 3 compatible. 
   - Fix the broken imports (e.g., Python 2 `urlparse`).
   - Ensure the protobuf serialization writes bytes correctly to standard output in Python 3 without crashing.

3. **Bash Processing Script**:
   - Write a Bash script at `/home/user/process_requests.sh`. Ensure it is executable.
   - The script must read URLs line-by-line from `/home/user/urls.txt`.
   - **Rate Limiting**: Enforce a strict rate limit of 1 request processed per second. The script must pause for exactly 1 second *before* processing each URL.
   - **Memory Profiling**: For each URL, execute the updated Python 3 `legacy_parser.py` script, passing the URL as the first argument. Profile the memory of this Python execution using `/usr/bin/time -v`.
   - **Logging**: For each URL processed, extract the domain from the URL using Bash or standard Linux tools (like `awk` or `sed`), and extract the "Maximum resident set size (kbytes)" from the `time -v` output. 
   - Append a line to `/home/user/processing.log` in the exact following format:
     `Domain: <domain> | URL: <url> | PeakMem: <kb> KB`
     *(Note: `<kb>` should be the integer value of the maximum resident set size)*

Example log output line:
`Domain: api.example.com | URL: https://api.example.com/v1/users | PeakMem: 12456 KB`

**Initial Files Provided to You**:
- `/home/user/request.proto`
- `/home/user/legacy_parser.py`
- `/home/user/urls.txt`

You must use `python3` to run the python scripts. Ensure your Bash script completes all tasks and generates the log file correctly.