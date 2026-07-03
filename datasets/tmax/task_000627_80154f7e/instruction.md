You are acting as a database administrator tasked with optimizing and deploying a querying service. 

We have a SQLite database located at `/home/user/data.db` that contains semi-structured data (NoSQL-style JSON columns). 
You need to build a C++ data processing engine that queries this database, performs a complex join and aggregation, and exposes the results via an HTTP service.

However, the documentation for the database schema has been lost, and all we have is an architecture diagram image located at `/app/schema.png`. 

Your tasks are:
1. **Reverse Engineer Data Model**: Analyze `/app/schema.png` (you can use `tesseract` or other tools) to determine the table names, join keys, and the JSON properties you need to aggregate.
2. **Build Query Engine**: Write a C++ program (e.g., `engine.cpp`) that queries the SQLite database. You will need to use SQLite's JSON functions to perform an aggregation pipeline (extracting values from the JSON arrays/objects, joining the two tables, and calculating the results). You must compile this to an executable `/home/user/engine`.
3. **HTTP Service**: Expose your C++ engine via an HTTP server listening on `127.0.0.1:8080`. You may write a simple Python wrapper (e.g., using `http.server` or `Flask`) that parses incoming requests, invokes your C++ binary, and returns the JSON response. The server must accept `GET /user_stats?user_id=<id>` and return a JSON response exactly matching the required output schema derived from the image. 
4. **Output Schema Validation**: Ensure the HTTP response sets the `Content-Type: application/json` header and returns valid JSON. 

Constraints & Details:
- The `sqlite3` development headers are available. You can compile your C++ code with `g++ engine.cpp -lsqlite3 -o engine`.
- The database contains a large number of rows; your query must be efficient.
- Ensure the server stays running in the background so that our automated verification can issue HTTP requests to it.

Start by examining the image to understand the schema and the specific metric you need to aggregate.