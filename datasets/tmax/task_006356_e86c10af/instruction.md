You are a web developer working on a backend feature that offloads a heavy mathematical data-encoding step to a C library for performance reasons. 

Your task is to write a script in a language of your choice (e.g., Python, Ruby, Node.js) and a C library to fulfill the following requirements:

1. **Custom Data Structure & FFI C Library:**
   Create a C file at `/home/user/libmath_encode.c`.
   It must define a custom struct named `MathBuffer` containing exactly two fields:
   - A pointer to unsigned character data (`unsigned char* data`)
   - The length of the data (`int length`)
   
   Implement a function with the signature `MathBuffer* encode_data(const char* input, int key)`.
   This function should allocate a new `MathBuffer` and its internal `data` array. 
   The encoding logic must populate the `data` array such that for each character in the `input` string:
   `encoded_byte[i] = (ASCII_value(input[i]) * key + i) % 256`
   *(Where `i` is the zero-based index of the character).*

2. **Compilation:**
   Compile the C code into a shared library at `/home/user/libmath_encode.so`.

3. **URL Parsing & Script Execution:**
   I have placed a file at `/home/user/request.txt` containing a single line with a URL, for example: `http://api.local/v1/math_encode?data=HelloWorld&key=5`
   
   Write a script at `/home/user/process_request` (make it executable and add a shebang). 
   When executed without arguments, this script must:
   - Read the URL from `/home/user/request.txt`.
   - Parse the URL to extract the `data` string and the integer `key`.
   - Use Foreign Function Interface (FFI, ctypes, FFI, etc.) to load `/home/user/libmath_encode.so` and call the `encode_data` function with the extracted `data` and `key`.
   - Read the resulting buffer from the returned `MathBuffer` struct.
   - Encode the resulting bytes as a continuous lowercase hexadecimal string (e.g., `1a2b3c...`).
   - Write ONLY the final hex string to `/home/user/result.txt`.

Ensure your script handles the FFI struct mapping correctly to extract the bytes and length. You can use any standard libraries available in your chosen language's standard installation.