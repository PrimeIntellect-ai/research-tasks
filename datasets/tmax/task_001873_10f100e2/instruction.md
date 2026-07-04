You are an analyst tasked with processing a dataset of hierarchical relationships. 

We have provided a vendored CSV parsing library at `/app/vendored/simple_csv_parser`. However, the library is currently not building due to an issue with its `Makefile`. You must first identify and fix the perturbation in the library's build process so you can compile it.

Once the library is working, use it to write a C program that reads two CSV files located at `/home/user/nodes.csv` and `/home/user/edges.csv`. The files describe a directed graph:
- `nodes.csv` has columns: `id,name`
- `edges.csv` has columns: `parent_id,child_id`

Your C program must build the graph in memory and then start a TCP server listening on port `8080` on `localhost`. 

The server must accept incoming TCP connections and read queries formatted as `GET_DESCENDANTS <id>\n`. 
For each query, your server must compute the complete set of descendants (children, children of children, etc.) for the given node `id`.
The server should respond with a comma-separated list of the descendant IDs in lexicographical order, followed by a newline (`\n`), and then keep the connection open for further queries. If the node has no descendants or does not exist, return `NONE\n`.

Write your server code in `/home/user/graph_server.c`, compile it linking against the fixed vendored library, and leave the server running in the background. Write a log of all incoming queries to `/home/user/query_log.txt`.