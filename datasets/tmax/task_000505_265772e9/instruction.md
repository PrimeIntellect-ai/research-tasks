You are an operations engineer debugging a Python application that interfaces with a legacy C library. The application processes streaming data blocks, validates requests, and offloads processing to the C library. 

Currently, the application cannot even build properly due to a C library linking issue. You need to fix the build, then write the parsing and validation logic to complete the pipeline.

You have the following workspace under `/home/user/app/`:
1. `/home/user/app/legacy/libprocessor.so`: A pre-compiled C library.
2. `/home/user/app/legacy/processor.h`: The header file containing the signature `int process_data(const char* data);`
3. `/home/user/app/setup.py`: A setuptools script intended to build a Python C-Extension `_legacy_wrapper` wrapping the C library. 
4. `/home/user/app/wrapper.c`: The C-Extension source code.
5. `/home/user/app/stream.log`: A log file containing network payload data.

**Your Tasks:**

1. **Fix the Build System (Linking Issue):**
   The `setup.py` script fails to link against `libprocessor.so` properly. When imported in Python, it either fails to build or throws an `ImportError: libprocessor.so: cannot open shared object file` because the runtime loader cannot find the library. Fix `/home/user/app/setup.py` so that it compiles correctly and permanently encodes the path to the library into the built extension (do NOT use `LD_LIBRARY_PATH` or copy the `.so` file). Run `python3 setup.py build_ext --inplace` to build it.

2. **Implement the State Machine Parser & Rate Limiter:**
   Write a Python script `/home/user/app/main.py` that reads `/home/user/app/stream.log`.
   The log file contains a custom protocol with the following structure:
   - A block starts with a line containing `START <IP_ADDRESS>`
   - Followed by 1 or more lines starting with `PAYLOAD:`
   - A block ends with a line containing `END`
   
   Your script must process this file line-by-line using a state machine (do not load the entire file into memory at once or use complex regexes spanning multiple lines). 
   
   While parsing, apply a strict **rate limit**: an IP address may process a maximum of 2 blocks. Any subsequent blocks from an IP that has already reached the limit of 2 must be completely ignored.

3. **Process Valid Blocks:**
   For each valid (not rate-limited) block, concatenate the payload strings (the text *after* `PAYLOAD:`, keeping the exact case and spaces, but removing the `PAYLOAD:` prefix and strip the trailing newlines). Pass this concatenated string to the newly built C-extension:
   `import _legacy_wrapper`
   `result = _legacy_wrapper.process(concatenated_payload)`

4. **Output:**
   Write the integer results returned by the C-extension for each processed block, in the order they appear, into `/home/user/app/results.txt`. Each integer should be on its own line.