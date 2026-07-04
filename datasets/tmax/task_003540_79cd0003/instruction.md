You are tasked with integrating a legacy user account system running in a QEMU Virtual Machine with a new modern API, as part of your site administrator duties. 

You need to perform the following steps:

1. **Network & VM Setup**: 
   The legacy system runs in a QEMU VM that requires a TAP interface named `tap0` to communicate with the host. 
   - Create a TAP interface named `tap0`.
   - Assign the IP address `10.0.0.1/24` to `tap0` and bring it up.
   - Once the interface is ready, execute `/app/start_services.sh` (already provided). This script will start a local API server on `127.0.0.1:8080` and boot the QEMU VM. The VM statically assigns itself `10.0.0.2` and listens on TCP port `9999`.

2. **Develop the User Data Parser (C)**:
   The legacy VM streams user account dumps over `10.0.0.2:9999` in a custom binary format. You must write a C program at `/home/user/parser.c` and compile it to `/home/user/parser`. This program will read binary data from `stdin` and print formatted text to `stdout`.
   
   **Binary Format Specification (per record)**:
   - `uid`: 4 bytes, Big-Endian unsigned integer.
   - `name_len`: 1 byte, unsigned integer (represents length of username, guaranteed to be between 0 and 31).
   - `username`: `name_len` bytes of ASCII characters.
   - `perms`: 2 bytes, Little-Endian unsigned integer.
   
   The program must read records continuously until EOF. For each successfully read record, it must print exactly:
   `UID:<uid> UNAME:<username> PERMS:<perms_in_hex_lowercase_4_digits>`
   Followed by a newline.
   
   If it encounters a partial record (e.g., hits EOF in the middle of a record), it must print `INVALID` and exit immediately (return code 0).
   
   *Note: Your compiled program must be bit-exact in its input/output behavior compared to our reference implementation. A stripped reference binary is available at `/app/oracle_parser` for you to test against.*

3. **Automation Script**:
   Write a robust bash script at `/home/user/sync.sh` that:
   - Connects to the legacy VM at `10.0.0.2:9999` (e.g., using `nc`).
   - Pipes the binary stream through your compiled `/home/user/parser`.
   - Sends the resulting text output via an HTTP POST request to `http://127.0.0.1:8080/sync` using `curl` with the `--data-binary` flag (the payload should be the exact text output of your parser).

Ensure `/home/user/sync.sh` is executable. 

Your success will be evaluated based on:
1. The functional correctness of your C parser against a strict random fuzzer.
2. The end-to-end multi-service flow successfully triggering the expected state in the local API.