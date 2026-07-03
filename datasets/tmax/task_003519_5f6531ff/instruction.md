You are a support engineer tasked with replacing a legacy diagnostic daemon that has been crashing in production. 

We recently received a bug report regarding this crash. The only information we have about the deployment environment's required authentication token is in a screenshot of the support ticket, located at `/app/ticket.png`.

Additionally, we have the crashing legacy binary at `/app/legacy_diagd`. We do not have the source code. 
Through preliminary analysis, we know:
1. The daemon accepts TCP connections.
2. It expects an authentication line: `AUTH <TOKEN>\n`, where `<TOKEN>` is the exact token from the image.
3. It then expects a series of commands in a custom format. Each command line starts with a 3-character string, a space, a 2-byte hex length, a space, and the payload. E.g., `CMD 0004 ping\n`.
4. The legacy binary crashes due to an integer overflow/parsing edge-case when the hex length is artificially large (e.g., `CMD FFFF payload...`), which hackers have been exploiting.

Your task:
1. Extract the authentication token from `/app/ticket.png`.
2. Reverse engineer and fuzz `/app/legacy_diagd` if you need more details about the expected responses (though the description above gives you the core protocol). 
3. Write a replacement daemon in C from scratch. Save the source code at `/home/user/new_diagd.c` and compile it to `/home/user/new_diagd`.
4. The new daemon must listen on TCP `127.0.0.1:8888`.
5. It must accept the `AUTH` command with the correct token (respond with `AUTH_OK\n`). If the token is wrong, respond with `AUTH_FAIL\n` and close the connection.
6. It must accept `CMD` packets. If the hex length exceeds 1024 (`0400`), it must cleanly respond with `ERR_TOO_LARGE\n` and ignore the payload, avoiding the crash present in the legacy version.
7. For valid `CMD` packets, it should respond with `CMD_RECV <length_in_decimal>\n`.

Start the daemon in the background before completing your task. Ensure it binds to `127.0.0.1:8888`.