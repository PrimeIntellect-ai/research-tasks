You are a QA engineer setting up a test environment for a legacy web security authentication flow. We need a lightweight mock AuthZ service written in C that speaks our legacy custom binary protocol.

First, examine the architectural diagram image located at `/app/authz_spec.png`. You will need to extract two critical pieces of information from this image (you can use `tesseract` to read the text):
1. The TCP Port the mock service should listen on.
2. The `SERVICE_ID` string, which acts as the valid authentication token.

Next, implement the mock service in C at `/home/user/mock_authz.c`. 
The service must bind to `127.0.0.1` on the port extracted from the image.
It must accept incoming TCP connections and process our custom binary serialization format:
- **Header (4 bytes)**: Magic number `0x4155545A` (ASCII "AUTZ").
- **Length (2 bytes, big-endian)**: The length of the payload.
- **Payload (variable length)**: A raw string containing exactly the token.

When a client sends a payload, your C program must deserialize the packet into a custom C data structure. 
- If the extracted payload string exactly matches the `SERVICE_ID` from the image, the server must reply with a 4-byte success code: `0x4F4B4159` (ASCII "OKAY") and close the connection.
- If the payload does not match, or if the magic number is incorrect, it must reply with a 4-byte failure code: `0x4641494C` (ASCII "FAIL") and close the connection.

Finally, write a CI/CD build script at `/home/user/build_and_deploy.sh` that:
1. Compiles `/home/user/mock_authz.c` into an executable at `/home/user/mock_authz` using `gcc` (with `-Wall -Wextra`).
2. Starts the compiled binary in the background.
3. Saves the process ID of the running service to `/home/user/mock_authz.pid`.

Make sure to run your build script so the service is actively listening when you finish the task.