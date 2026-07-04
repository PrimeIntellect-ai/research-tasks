You are an engineer tasked with porting a high-performance URL filtering tool to a minimal container environment. Because standard tools like Nginx are not available, you must implement a lightweight Python reverse proxy that uses a custom-built C extension for high-speed URL path matching.

Your task consists of three phases:

**Phase 1: Custom Data Structure in C (Prefix Trie)**
Create a file `/home/user/trie.c` that implements a Prefix Trie data structure for fast prefix matching. It must expose exactly these C functions:
1. `void* trie_create();` - Allocates and returns a pointer to a new, empty trie.
2. `void trie_insert(void* trie, const char* prefix);` - Inserts a string prefix into the trie.
3. `int trie_check(void* trie, const char* path);` - Checks if the given `path` starts with ANY of the prefixes stored in the trie. Returns `1` if a matching prefix is found, and `0` otherwise.

Create a `Makefile` in `/home/user` that compiles `trie.c` into a shared library named `/home/user/libtrie.so`. Running `make` should perform the compilation. 

**Phase 2: Python FFI and Reverse Proxy**
Write a Python 3 script `/home/user/proxy.py` using only standard libraries. 
The script must act as a reverse proxy server listening on `127.0.0.1:8080`. 
When the script starts, it must:
1. Use `ctypes` to load `/home/user/libtrie.so`.
2. Initialize a trie using `trie_create`.
3. Read the file `/home/user/blocked.txt` (which contains one path prefix per line, ignoring empty lines) and insert each prefix into the trie using `trie_insert`.

For every incoming HTTP GET request:
1. Extract the request path.
2. Use `trie_check` to see if the path starts with any blocked prefix.
3. If it is blocked (returns 1), immediately respond with an HTTP `403 Forbidden` status and the exact text `Blocked by Trie`.
4. If it is not blocked (returns 0), proxy the GET request to the backend server running at `http://127.0.0.1:9090` (preserving the exact path). Return the backend's HTTP status code, headers, and body back to the original client.

**Environment details:**
- The backend server will be running on `127.0.0.1:9090` (you do not need to implement the backend, just proxy to it).
- You must create the `Makefile`, `trie.c`, and `proxy.py` files.
- Ensure your proxy can handle basic GET requests and properly close connections.

Complete these steps and ensure the proxy runs flawlessly.