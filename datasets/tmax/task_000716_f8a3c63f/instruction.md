As a storage administrator, I've inherited a server with a directory full of archived logs taking up unnecessary space in `/home/user/logs/`. These files all end in `.zlog`. 

First, I need you to standardize our archive naming by bulk-renaming all `*.zlog` files in `/home/user/logs/` to have the extension `*.legacy.z`.

Second, these files are compressed using a legacy, proprietary tool. We found the stripped extraction binary at `/app/bin/zdecoder`. If you run it with a file as an argument (e.g., `/app/bin/zdecoder filename`), it decompresses the file and dumps the raw content to standard output. However, the internal text is encoded in UTF-16LE, which our modern logging stack cannot read natively.

I need you to write a C program at `/home/user/log_server.c` (and compile it to `/home/user/log_server`) that acts as a bridge. The program must:
1. Run as a daemon/server listening on TCP port `9090`.
2. Accept incoming client connections.
3. Read a single line from the client containing the absolute path to a legacy log file (e.g., `/home/user/logs/app1.legacy.z\n`).
4. Execute `/app/bin/zdecoder` on the requested file, stream its output, convert the encoding from UTF-16LE to UTF-8 on the fly (using streaming I/O to avoid high memory consumption), and send the UTF-8 text back over the client socket.
5. Close the client connection after streaming is complete.

Ensure the server is running in the background when you complete your task so we can query it.