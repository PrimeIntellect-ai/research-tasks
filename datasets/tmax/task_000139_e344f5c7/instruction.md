You are a web developer building a high-throughput real-time IP analytics feature for a web application. 

You have been given a Go component that concurrently generates and aggregates incoming IP addresses. You need to orchestrate the build system, design a custom algorithmic data structure in Python to query these IPs, and integrate the components.

Perform the following tasks:

1. **Polyglot Build & Cross-Compilation**:
   There is a Go source file located at `/home/user/go_src/aggregator.go`. 
   Write a build script (or execute commands) to compile this Go code into two artifacts in the `/home/user/build/` directory:
   - A C-shared library for Linux (`linux/amd64`) named `aggregator.so`.
   - A standard executable binary for Windows (`windows/amd64`) named `aggregator.exe`.
   *(Note: Ensure you set the correct Go environment variables for cross-compilation and CGO)*.

2. **Custom Data Structure Design (`/home/user/ip_trie.py`)**:
   Implement a Python module named `ip_trie.py` containing a class `IPTrie`. 
   The `IPTrie` must efficiently store IPv4 addresses and support fast subnet querying. It must implement:
   - `insert(ip_address: str)`: Inserts a standard IPv4 address string (e.g., "192.168.1.5").
   - `count_subnet(cidr: str) -> int`: Returns the total number of inserted IPs that fall within the given CIDR block (e.g., "192.168.1.0/24"). Do not use naive list comprehension filtering; use the underlying tree/trie algorithmic structure.

3. **Integration (`/home/user/app.py`)**:
   Write a Python script named `app.py` that does the following:
   - Uses the `ctypes` library to load the `/home/user/build/aggregator.so` C-shared library.
   - Calls the exported Go function `GetIPs`. This function takes no arguments and returns a C string (`c_char_p`) containing a comma-separated list of IP addresses.
   - Parses the returned string, instantiates an `IPTrie`, and inserts all the parsed IP addresses into the trie.
   - Queries the trie for the following CIDR subnets:
     - "10.0.0.0/8"
     - "172.16.0.0/12"
     - "192.168.1.0/24"
   - Writes the results to a JSON file at `/home/user/results.json` in this exact format:
     ```json
     {
       "10.0.0.0/8": <count>,
       "172.16.0.0/12": <count>,
       "192.168.1.0/24": <count>
     }
     ```

Run your build process, execute `app.py`, and ensure `/home/user/results.json` is correctly generated.