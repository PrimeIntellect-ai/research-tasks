You are an expert systems programmer debugging a complex C library ecosystem with deeply nested linking dependencies. You need to build a Python tool that parses linker output, resolves dependency paths, and serves queries over WebSockets.

Your task is to write the backend server and its test suite.

**Step 1: The Parser and Graph Resolution**
Create a Python file `/home/user/analyzer.py`.
Implement a state-machine based parser inside `def parse_ldd(filepath: str) -> dict:` that reads a custom linker dump file. 
The dump file `/home/user/ldd_dump.txt` will look like this:
```
[libapp.so]
    linux-vdso.so.1 =>  (0x00007ffe3b1bc000)
    libutil.so => /usr/lib/libutil.so (0x00007f3c0a5d4000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f3c0a3e2000)
[libutil.so]
    libcore.so => /usr/lib/libcore.so (0x00007f3c0a5d4000)
```
- A line starting with `[` and ending with `]` represents a target library.
- Subsequent indented lines represent its dependencies.
- You must extract the library name before the `=>` (e.g., `libutil.so`).
- **Ignore** `linux-vdso.so.1` and `libc.so.6`.
- Return a dictionary mapping each target library to a list of its dependencies.

Implement `def find_shortest_path(graph: dict, start: str, target: str) -> list:` which performs a graph traversal (e.g., BFS) to find the shortest dependency path from `start` to `target`. Return the path as a list of strings (e.g., `['libapp.so', 'libutil.so', 'libcore.so']`). Return an empty list if no path exists.

**Step 2: WebSocket Server**
Create `/home/user/server.py`. 
Using the `websockets` package (you may install it via `pip install websockets`), write an asyncio WebSocket server that runs on `localhost:8765`.
- On startup, it should load and parse `/home/user/ldd_dump.txt`.
- When a client connects and sends a JSON payload like `{"start": "libapp.so", "target": "libcore.so"}`, the server should calculate the path and reply with a JSON message: `{"path": ["libapp.so", "libutil.so", "libcore.so"]}`.
- Do NOT start the server automatically if the file is imported. Only run the server if `__name__ == "__main__"`.

**Step 3: Unit Testing & Mocks**
Create `/home/user/test_analyzer.py`.
Write a test suite using Python's built-in `unittest` and `unittest.mock`.
1. Write a test for `parse_ldd` that uses `mock_open` to simulate reading a dump file without hitting the disk, verifying the state machine parser correctly ignores `libc` and builds the dictionary.
2. Write a test for `find_shortest_path` using a hardcoded fixture graph to verify correct traversal, including a case where no path exists.

Finally, execute your analyzer to find the path from `libfront.so` to `libbase.so` based on the file `/home/user/ldd_dump.txt`, and save the resulting list as a JSON array in `/home/user/result.json`.