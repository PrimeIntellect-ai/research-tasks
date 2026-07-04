You are assisting a compliance officer auditing an internal system's access topology. 

We have recovered a scanned image of the legacy network access diagram, located at `/app/topology.png`. 

Your objectives are:
1. Extract the access rules from the image. The image contains text where each line specifies a directed access rule in the exact format `Source->Destination` (e.g., `X->Y`). The nodes are single uppercase letters representing different secure enclaves.
2. Write a C program (e.g., `audit_server.c`) that reads these extracted rules and builds an in-memory directed graph.
3. The C program must implement and start a minimal HTTP server listening on `127.0.0.1:8080`.
4. The server must handle `GET` requests to the endpoint `/audit/shortest_path?src=<NODE>&dst=<NODE>` (where `<NODE>` is a single uppercase letter).
5. For a valid request, compute the shortest path (minimum number of hops) from `src` to `dst`.
6. Respond with an `HTTP/1.1 200 OK` status, a `Content-Type: application/json` header, and a JSON body with the exact schema:
   `{"path": ["A", "B", "C"], "length": 2}`
   If no path exists between the nodes, the response must be:
   `{"path": [], "length": -1}`
   If multiple shortest paths exist, return any one of them.
7. Compile and run the server in the background so it is ready to accept requests.

Ensure your C code gracefully handles multiple sequential HTTP requests and properly parses the query string. You may use `tesseract` to read the image text. Use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `sys/socket.h`, `netinet/in.h`, etc.) for the server implementation.