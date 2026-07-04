You are tasked with setting up a backup archiving utility for our logging infrastructure. We need to process an incoming stream of JSON logs, extract specific data, compress it using a specific library, and output a custom binary archive format.

However, the specific compression library we need to use, `brotli-1.1.0`, has been pre-vendored for you at `/app/brotli-1.1.0` because we are running in an air-gapped environment. The vendor provided a slightly broken `setup.py` which fails to build the C extension. 

Here are your objectives:
1. Identify and fix the deliberate typo/error in `/app/brotli-1.1.0/setup.py` so that it builds correctly, and install the package into your Python environment.
2. Write a Python script at `/home/user/archive.py` that reads line-delimited JSON logs from `stdin`. 
3. Each line is a valid JSON object containing at least a `"message"` string field. 
4. For each JSON object, extract the `"message"` string, **reverse the characters** in the string (e.g., "Hello" becomes "olleH"), and encode it as UTF-8.
5. Compress the resulting UTF-8 byte string using `brotli.compress` with `quality=4`.
6. Write the result to `stdout` in the following binary format for each processed line:
   - A 4-byte unsigned little-endian integer representing the size of the compressed payload.
   - The compressed payload bytes.
7. Your script must process the stream continuously (streaming I/O) rather than loading all of `stdin` into memory at once, and gracefully exit when `stdin` is closed.

Ensure your script operates exactly as specified, as it will be rigorously tested against a reference implementation with thousands of randomized logs.