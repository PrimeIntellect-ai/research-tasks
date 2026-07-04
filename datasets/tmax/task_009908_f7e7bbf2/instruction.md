You are a platform engineer maintaining a CI/CD pipeline. Part of the pipeline requires building a C shared library that performs fast string transformations, which is later invoked by Python scripts using `ctypes`.

Your task is to write the C library and its build script to satisfy the pipeline's requirements.

1. Create a C source file at `/home/user/transform.c`. 
   It must export a single function with the following signature:
   `int transform_string(const char* input, char* output);`
   
   The function should do the following:
   - Reverse the null-terminated `input` string.
   - Prepend a prefix to the reversed string based on the `PIPELINE_ENV` macro.
   - If `PIPELINE_ENV` is defined (e.g., as `"CI"` or `"PROD"`), prepend that exact string followed by an underscore `_`.
   - If `PIPELINE_ENV` is not defined, prepend `"DEFAULT_"`.
   - Write the final resulting string (prefix + reversed input) into the `output` buffer. You may assume `output` is large enough.
   - Return the total length of the newly constructed string in `output`.

2. Create a bash build script at `/home/user/build.sh`.
   - The script must take exactly one argument (e.g., `CI` or `PROD`).
   - It should compile `/home/user/transform.c` into a shared library named `/home/user/libtransform.so`.
   - It must pass the argument to the C compiler to define the `PIPELINE_ENV` macro as a string literal matching the argument.
   - Make sure the script is executable.

3. After writing the code and build script, run `./build.sh PROD`.

4. Finally, run the provided Python FFI verification script at `/home/user/verify.py` using `python3 /home/user/verify.py`. This script will load your shared library, call `transform_string` with the input `"engineer"`, and write the output and return value to `/home/user/result.log`.

Do not modify `/home/user/verify.py`. Ensure `/home/user/result.log` is generated successfully.