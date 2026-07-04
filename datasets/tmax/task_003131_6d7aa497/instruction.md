You are a data engineer building an ETL pipeline. Your goal is to implement a robust, high-performance data aggregation service in C that processes streaming graph edge data.

You have been provided with an image at `/app/rule.png` which contains a visual representation of the specific edge type you need to filter for. The text in the image is formatted as `FILTER_TYPE=<type>`.

Your task:
1. Write a C program (you may use helper shell scripts/commands like `tesseract` to OCR the image) that acts as a raw TCP server listening on `127.0.0.1:7070`.
2. When a client connects, it will send graph data in CSV format, where each line represents an edge:
   `source_node,target_node,edge_type,weight`
   (The stream is terminated by the client closing the write half, or sending an EOF. You should read until EOF on the connection).
3. The server must filter the edges to only include those matching the `edge_type` extracted from `/app/rule.png`.
4. Perform an analytical aggregation: for the filtered edges, calculate the total sum of `weight` for each `source_node`.
5. Find the `source_node` with the highest total weight.
6. The server must send exactly one line back to the client over the TCP connection before closing it:
   `MAX_SOURCE: <source_node>, AMOUNT: <total_weight>\n`
   (If there are no matching edges, return `MAX_SOURCE: NONE, AMOUNT: 0\n`).

Constraints:
- You must write the core TCP server in C. You can compile it using `gcc`.
- You can use standard Linux utilities (e.g., `tesseract` for OCR) invoked from your C code.
- The C server must be running and listening on port 7070 in the background so that the verification process can connect to it.

Start by examining the image, writing your server, compiling it, and running it in the background. Ensure it cleanly handles multiple sequential client connections if necessary.