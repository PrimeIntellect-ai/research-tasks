You are a systems programmer working on a web application that relies on a C shared library to perform fast deserialization of user session data. Recently, the application has been crashing with segmentation faults due to malformed, oversized session payloads. Furthermore, a recent update to the build system has caused linking issues because functions are no longer being exported correctly from the shared library.

Your objective is to fix the C library, recompile it, and write a Python test fixture to verify the fix.

Here is your setup:
The source code is located at `/home/user/src/session_parser.c`:
```c
#include <string.h>
#include <stdlib.h>

typedef struct {
    int user_id;
    char username[16];
    int is_admin;
} Session;

int parse_session(const char* payload, Session* out_session) {
    char buffer[32];
    strcpy(buffer, payload);
    
    char* token = strtok(buffer, ",");
    if (!token) return -1;
    out_session->user_id = atoi(token);
    
    token = strtok(NULL, ",");
    if (!token) return -1;
    strncpy(out_session->username, token, 15);
    out_session->username[15] = '\0';
    
    token = strtok(NULL, ",");
    if (!token) return -1;
    out_session->is_admin = atoi(token);
    
    return 0;
}
```

The Makefile at `/home/user/src/Makefile`:
```makefile
all:
	gcc -shared -fPIC -fvisibility=hidden -o libsession.so session_parser.c
```

Task Requirements:
1. **ABI Management:** The Makefile compiles with `-fvisibility=hidden`, meaning `parse_session` is not exported, leading to an `AttributeError` when loaded in Python. Modify `session_parser.c` to properly export the `parse_session` function so it is accessible from the shared library.
2. **C Memory Safety Repair:** The `strcpy` function in `parse_session` causes a buffer overflow when a long payload is provided. Fix the C code to safely handle payloads of any length without crashing or leaking memory. Ensure that valid fields appearing after a long username (like `is_admin`) are still correctly parsed.
3. Recompile the library by running `make` in `/home/user/src/`.
4. **Test Fixture Setup:** Write a Python test script at `/home/user/test_sec.py`. 
    - Use the `ctypes` module to load `/home/user/src/libsession.so`.
    - Define the corresponding `Session` structure in Python.
    - Call `parse_session` with this exact malicious payload: `"42,administratoooooooooooooooooooooooooooooooooooor,1"`.
    - Catch any errors, ensure the call succeeds without crashing, and write the parsed `user_id` and `is_admin` to `/home/user/result.log` in exactly this format: `user_id: 42, is_admin: 1`.

Run your Python test script to generate the log file.