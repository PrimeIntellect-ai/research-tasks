You are a DevOps engineer tasked with deploying and debugging `minilogd`, a custom lightweight log-aggregation daemon written in C. 

The source code for the daemon is vendored at `/app/minilogd-1.0`. It consists of a TCP server for ingesting raw logs and an HTTP server for querying them.

Currently, the service has several critical issues preventing deployment:

1. **Service Hang on Queries**: The query parser (`src/query.c`) has a bug. When users submit complex queries containing nested parentheses (e.g., `(level=ERROR AND (app=frontend OR app=backend))`), the parsing engine hangs and consumes 100% CPU. You need to debug and fix this infinite loop / recursion issue in the parser.
2. **Incorrect Query Results**: The log filtering mechanism (`src/db.c`) has a logic bug. When querying for specific log severity levels, the results are inconsistent and often include unrelated log levels. Debug the query execution logic and fix it so it strictly matches the requested severity levels.
3. **Missing Authentication Token**: The HTTP query API is protected by a Bearer token. The token validation logic is compiled into a proprietary shared object at `lib/libauth.so` (there is no source code for this file, only the `include/auth.h` header). You must reverse engineer this binary to determine the hardcoded master token. 

**Your objectives:**
1. Fix the C code in `/app/minilogd-1.0/src/query.c` and `/app/minilogd-1.0/src/db.c`.
2. Reverse engineer `lib/libauth.so` to discover the plaintext token. Write this exact token to `/home/user/admin_token.txt`.
3. Recompile the project using the provided `Makefile`.
4. Start the `minilogd` daemon in the background. Ensure it binds to `127.0.0.1:8080` for the TCP ingest server and `127.0.0.1:8081` for the HTTP API server. Leave the process running.

Do not modify the `libauth.so` binary or bypass the authentication check in the server; you must find the actual valid token.