You are an IT support technician investigating a critical issue with our internal Ticket Management API daemon. 

We have a vendored copy of the `ticket_server` source code located at `/app/vendored/ticket_server/`. Recently, a developer tried to optimize memory usage by changing a data type related to ticket priority calculations. Since then, the server intermittently crashes or returns garbled data when processing high-precision timestamps and priorities.

Your objectives:
1. **Secret Recovery:** The daemon requires an Admin authentication token to accept connections. This token was accidentally committed in a configuration file in the Git history of the `/app/vendored/ticket_server/` repository, but was subsequently removed. Find this token and write it exactly as it appears into `/home/user/admin_token.txt`.
2. **Error Diagnosis & Fix:** Use standard debugging tools (like GDB) to reproduce the intermittent crash when parsing ticket priorities. The issue is suspected to be a precision loss or memory corruption bug introduced by the recent `float` vs `double` type changes in `server.c`. Fix the bug in the C source code so that it correctly parses high-precision priorities without corrupting the stack.
3. **Deployment:** Recompile the server using the provided `Makefile`. Start the daemon in the background so it listens on `127.0.0.1:9090`. The server binary accepts the port as an argument: `./ticket_server 9090`.

Ensure the server remains running. Do not modify the expected JSON response format. An automated verifier will attempt to send HTTP GET requests to `/api/tickets` on port 9090 using the recovered authentication token.