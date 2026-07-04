You are a database reliability engineer handling backups for a proprietary graph database system. A recent catastrophic failure requires you to restore and verify a raw binary backup file (`/home/user/backup.dat`). 

To read this backup, we use a vendored C library located at `/app/libgraphdump-1.2.0/`. However, the library currently fails to compile due to a configuration issue in its `Makefile`. 

Your objectives are:
1. Identify and fix the build issue in `/app/libgraphdump-1.2.0/` so you can successfully build the `libgraphdump.so` shared library.
2. Write a C program at `/home/user/backup_verifier.c` that links against this library to parse the `/home/user/backup.dat` file. The library provides a `parse_graph_dump(const char* filename, Graph* g)` function (see `/app/libgraphdump-1.2.0/graphdump.h` for details).
3. Your C program must start a TCP server listening on `127.0.0.1:8080`.
4. The TCP server must accept incoming connections and process line-based text queries (ending with `\n`). The supported queries are:
   - `DEGREE <node_id>`: Return the degree (number of connected edges, treating the graph as undirected) of the given integer `node_id`. Reply with just the integer degree followed by a newline.
   - `PATH <node_id_A> <node_id_B>`: Return the shortest path length (number of edges) between the two nodes using Breadth-First Search. If the nodes are the same, return `0`. If there is no path, return `-1`. Reply with the integer length followed by a newline.
5. The server should stay running to handle multiple sequential queries from our automated verification system.

Compile your server program, start it in the background, and ensure it is listening on port 8080 before completing the task. 

Constraints:
- Only use standard C libraries (e.g., `stdio.h`, `stdlib.h`, `sys/socket.h`, etc.) and the provided `libgraphdump.so`.
- Do not modify the data in `backup.dat`.