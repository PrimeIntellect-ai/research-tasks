You are a Database Reliability Engineer managing a complex, multi-model backup system. Our backup metadata spans a relational database and a graph database. 

We have a legacy proprietary binary located at `/app/meta_bridge` that maps relational table names to their corresponding graph representation queries. Recently, a bug was discovered where querying the relational database with concurrent `JOIN` operations causes a deadlock in the backup manager. To mitigate this, we need to extract the graph pipeline using the binary, bypassing the relational engine's join planner.

Your task is to create a wrapper microservice that handles incoming relational join queries and safely converts them into graph traversal pipelines using the legacy binary.

Write and start a network service (in the language of your choice, e.g., Python, Node.js) that:
1. Listens on TCP port `127.0.0.1:8081`.
2. Accepts plain text TCP connections where the client sends a simple relational join query in the exact format: `SELECT * FROM <table> JOIN <table2> ON <condition>\n`
3. Parses the two table names (`<table>` and `<table2>`) from the query.
4. Executes the legacy binary `/app/meta_bridge` twice, once for each parsed table name, passing the table name as the single command-line argument (e.g., `/app/meta_bridge <table>`).
5. Captures the standard output of the binary, which will be a graph node identifier (a string).
6. Chains them together into a pipeline string in the exact format: `PIPELINE: <graph_node_1> -> <graph_node_2>\n`.
7. Sends this pipeline string back to the TCP client and closes the connection.

Ensure your service runs continuously and handles multiple sequential requests. You do not need to validate the SQL syntax beyond extracting the two table names around the `JOIN` keyword. Create your service script in `/home/user/service_wrapper` (any file extension is fine) and ensure it is running in the background. Write a log file to `/home/user/wrapper.log` recording each request received.