You are tasked with migrating a legacy Python 2 data processing service to Python 3 and securing its underlying C library.

The service consists of a C extension (`libcalc.c`) and a Python 2 wrapper (`api.py`) located in `/home/user/app`. The service reads a batch of requests from `/home/user/app/requests.json`. 

Currently, the system suffers from a few severe issues:
1. **Migration needed:** `api.py` is written in Python 2. You need to upgrade it to Python 3. Be careful with `ctypes` string handling, as Python 3 strings are Unicode and need to be explicitly encoded to bytes before being passed to C.
2. **Memory Safety:** The C library has a buffer overflow vulnerability. `libcalc.c` takes a string input and copies it into a fixed-size 11-byte buffer (10 chars + null terminator). You must fix `libcalc.c` to safely truncate any input string longer than 10 characters to exactly 10 characters before processing, ensuring it is properly null-terminated and doesn't write out of bounds. After fixing, recompile the shared library: `gcc -shared -fPIC libcalc.c -o libcalc.so`.
3. **Request Validation & Rate Limiting:** The Python service currently processes everything it receives. You must update `api.py` to enforce the following constraints:
   - **Validation:** The `data` field in the request must be strictly alphanumeric. If it contains spaces, punctuation, or special characters, the request should be rejected.
   - **Rate Limiting:** A single `user` can only make a maximum of 2 requests in total across the entire batch. Any subsequent requests by the same user must be rejected.

Modify `api.py` to write the outcome of every request in the exact order they appear in `requests.json` to `/home/user/app/results.log`. 
For each request, append a line in this exact format:
`USER:<user> STATUS:<ACCEPTED|REJECTED> RESULT:<integer_result_from_c_or_NONE>`

Example output line for an accepted request:
`USER:alice STATUS:ACCEPTED RESULT:945`
Example output line for a rejected request (failed validation or rate limited):
`USER:bob STATUS:REJECTED RESULT:NONE`

Once you have completed the fixes, run `python3 /home/user/app/api.py` to process the requests and generate the `/home/user/app/results.log` file.