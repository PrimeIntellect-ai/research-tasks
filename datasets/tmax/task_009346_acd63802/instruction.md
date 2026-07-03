You are a mobile build engineer maintaining a build pipeline. You need to implement a secure C library that validates and decodes asset URLs, and a Python script that interfaces with this C library using FFI (`ctypes`).

Your task:
1. Create a C library in `/home/user/libfetch.c`. It must implement the following function:
   `int validate_and_fetch(const char* url, char* output_buffer);`

   The function must:
   - **Rate Limiting**: Track the total number of times `validate_and_fetch` has been called in the current process using a static or global counter. If the function is called more than 3 times (i.e., on the 4th call and onwards), it must immediately return `-2` and not modify the `output_buffer`.
   - **URL Decoding**: Fully decode any percent-encoded characters (e.g., `%2F` to `/`, `%2E` to `.`) in the input `url`.
   - **Validation**: After decoding, check if the decoded URL strictly starts with `https://internal.build.corp/`. If it does not, return `-1` and do not modify the `output_buffer`.
   - **Success**: If the URL is valid and the rate limit is not exceeded, copy the decoded URL into `output_buffer` and return `0`.

2. Compile the C file into a shared library at `/home/user/libfetch.so`.

3. Create a Python script at `/home/user/build_pipeline.py` that uses `ctypes` to load `/home/user/libfetch.so` and calls `validate_and_fetch`. Provide a sufficiently large buffer (e.g., 256 bytes) for the output.

4. The Python script must test the following URLs in this exact order:
   1. `https://internal.build.corp/asset1.zip`
   2. `https://internal%2Ebuild%2Ecorp/asset2.zip`
   3. `https://external.com/%2E%2E/internal.build.corp/`
   4. `https://internal.build.corp/asset3.zip`
   5. `https://internal.build.corp/asset4.zip`

5. The Python script must log the results of these 5 calls to `/home/user/pipeline.log`. Each line in the log must exactly match the format:
   `URL: <original_input_url>, Status: <return_code>, Output: <output_buffer_string_if_success_else_empty>`

   For example, a failed validation should output: `URL: https://bad.com, Status: -1, Output: `

Run your Python script to generate the log file.