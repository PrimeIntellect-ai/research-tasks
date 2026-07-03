You are a build engineer responsible for fixing a broken C-based WebSocket security proxy. 

The project is located at `/home/user/ws_proxy`. It currently fails to build due to unresolved symbols and version conflicts in its local dependencies.

Here is the situation:
1. Inside `/home/user/ws_proxy/packages/`, there are multiple versions of pre-compiled static libraries: 
   - `libws` (versions v1, v2)
   - `libauth` (versions v1, v2, v3)
   - `libfilter` (versions v1, v2)
2. The `server.c` file relies on specific security and WebSocket functions. The provided `Makefile` is currently trying to link arbitrary versions of these libraries, causing compilation and linking to fail.
3. You must inspect the static libraries (e.g., using `nm`) to satisfy the symbol dependency constraints:
   - `server.c` requires the symbol `ws_init_secure`.
   - The version of `libws` containing `ws_init_secure` has an undefined reference to a specific authentication symbol.
   - The matching `libauth` version has an undefined reference to a strict filtering symbol.
   - Only one combination of `libws`, `libauth`, and `libfilter` satisfies all dependencies without undefined references.
4. Update the `Makefile` to link against the correct library versions so the project compiles successfully.
5. Build the proxy by running `make`. Start the resulting executable (`/home/user/ws_proxy/proxy_server`). It will listen on `ws://127.0.0.1:8080`.
6. To verify the proxy's Web Security filtering capabilities, act as a client. Send the following exact message over the WebSocket connection to the running server: 
   `{"type": "chat", "msg": "<script>alert(1)</script>"}`
7. Save the exact literal string response received from the WebSocket server into a file named `/home/user/ws_response.log`.

Requirements:
- Ensure the proxy server remains running in the background while you test it.
- Ensure the final `/home/user/ws_response.log` contains only the server's response payload.