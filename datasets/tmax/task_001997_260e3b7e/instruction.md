A researcher in our lab has been organizing a dataset of academic publications. They wrote a custom C++ in-memory graph query server to quickly find co-authors of specific researchers. 

However, the current implementation in `/home/user/graph_server.cpp` has a major bug: when querying for co-authors, the custom graph traversal logic accidentally computes an implicit Cartesian product (cross join) between the author's papers and all other papers in the dataset, leading to exponentially large, incorrect result sets and terrible performance. It also entirely lacks a required filtering rule.

Your task is to fix and deploy this service.

1. Inspect the C++ source code in `/home/user/graph_server.cpp`. You will see it loads data from `/home/user/dataset.csv` (format: `AuthorID,AuthorName,PaperID,PaperYear`).
2. Fix the graph projection and query logic in the `get_coauthors` function. It should use proper index-based traversal (adjacency lists) to only traverse papers the given author has actually written, and then find other authors who wrote those *same* papers.
3. The researcher left a sticky note with a critical filtering rule that must be applied to the output. This note has been scanned and saved as an image at `/app/filter_rule.png`. Extract the rule from this image and implement it in your C++ query logic. Only co-authors from papers matching this rule should be included.
4. The output must strictly follow this JSON schema validation structure:
   `{"author": "RequestedName", "coauthors": ["Name1", "Name2"]}`
   (Deduplicate the coauthor list, and do not include the original requested author in the coauthors list).
5. Compile the C++ program into an executable named `server` in `/home/user/`. Use `g++ -O3 -std=c++17` (a single-header HTTP library `httplib.h` is already in the directory).
6. Run the server. It must bind and listen for HTTP GET requests on `127.0.0.1:8080`.
7. The endpoint to serve is `/coauthors?name=<AuthorName>`. Leave the server running in the background.

Please fix the code, compile, and start the service.