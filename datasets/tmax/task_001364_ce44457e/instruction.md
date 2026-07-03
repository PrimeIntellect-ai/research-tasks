You are an integration developer responsible for testing a new API gateway routing module. 

We have a legacy routing logic currently implemented in Python, and we need to port it to a C shared library for performance, wrapped by a Python CLI tool using `ctypes`.

Here is what you need to do:
1. **Extract Constants**: There is an image at `/app/schema.png` containing configuration specifications. Extract the `API_BASE` URL and the `MIN_VERSION` semantic version constraint from this image using OCR (e.g., `tesseract`).
2. **Translate Code**: We have a reference Python implementation at `/home/user/reference.py` (which currently has placeholder constants). Translate the `process` function's logic into C. Your C code must be placed in `/home/user/librouter.c` and compiled into a shared library at `/home/user/librouter.so`. 
   - The C library must export a function with the signature: `char* process_route(const char* path, const char* version);`
   - You must correctly implement URL parameter parsing and semantic version comparison in C, exactly matching the behavior of the reference Python script.
   - Pay close attention to C memory safety and string manipulation. The returned string should be dynamically allocated.
3. **FFI Wrapper**: Create a Python command-line tool at `/home/user/router_cli.py`. 
   - It must take exactly two command-line arguments: `<path>` and `<version>`.
   - It must use `ctypes` to load `/home/user/librouter.so`, call `process_route`, print the returned string to standard output, and exit.

**Reference Implementation (`/home/user/reference.py`)**:
```python
import sys

# Replace these with the actual values from /app/schema.png
API_BASE = "PLACEHOLDER_URL" 
MIN_VERSION = "0.0.0"

def compare_versions(v1, v2):
    parts1 = [int(x) for x in v1.split('.')]
    parts2 = [int(x) for x in v2.split('.')]
    return parts1 >= parts2

def process(path, version):
    if not compare_versions(version, MIN_VERSION):
        return "ERROR: Version too old"
    
    if "?" in path:
        base_path, query = path.split("?", 1)
        params = query.split("&")
        param_str = ", ".join(params)
    else:
        base_path = path
        param_str = "none"
        
    return f"ROUTED: {API_BASE}{base_path} PARAMS: {param_str}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    print(process(sys.argv[1], sys.argv[2]))
```

Your final deliverable is the fully functional Python script at `/home/user/router_cli.py` that utilizes your compiled `/home/user/librouter.so`. An automated testing suite will aggressively fuzz your `router_cli.py` with random URLs and semantic versions to ensure it produces bit-exact equivalent output to our oracle reference binary. Ensure there are no segmentation faults or undefined behaviors.