You are a script developer writing utilities for a backend system. We have a legacy C function that performs custom URL-decoding, but it is currently crashing due to memory safety issues (buffer overflows) when processing long strings. 

Your objective is to fix the C code, compile it into a shared library, and write a Python script that uses this library via FFI (`ctypes`) to process a list of URL routes.

Here are the specific steps you must follow:

1. **Fix the C Code:**
   You will find a C source file at `/home/user/decoder.c`. It contains a function `char* decode_url_payload(const char* src)`. Currently, it uses a fixed-size local buffer `char buffer[32];` which causes a segmentation fault when processing long payloads. 
   - Fix the memory safety bug in `/home/user/decoder.c` by dynamically allocating the buffer or sizing it appropriately based on the input length `strlen(src)`. 
   - Make sure the function still correctly unescapes `%XX` hex sequences and `+` symbols.

2. **Compile the Shared Library:**
   Compile the fixed `decoder.c` into a shared library named `/home/user/libdecoder.so` using `gcc`.

3. **Write the Python Script (`/home/user/run.py`):**
   Create a Python script at `/home/user/run.py` that does the following:
   - Reads a list of URLs from `/home/user/urls.txt`.
   - Uses standard Python libraries (like `urllib.parse`) to parse each URL and extract the value of the `payload` query parameter.
   - Loads `/home/user/libdecoder.so` using `ctypes`.
   - Passes the extracted `payload` string to the `decode_url_payload` C function.
   - Retrieves the returned decoded string. (Make sure to set `restype = ctypes.c_char_p` so Python handles the pointer correctly).
   - Writes the decoded strings to `/home/user/results.txt`, outputting one decoded string per line in the exact same order as the URLs in `urls.txt`.

Ensure `/home/user/results.txt` contains exactly the decoded strings, one per line, with no extra formatting.