You are a data engineer tasked with rebuilding a critical ETL graph projection pipeline step. 

We recently lost the source code for a microservice that materializes a specific graph projection from our raw edge streams. Fortunately, we have a screenshot of the original Cypher query that defined the projection logic, located at `/app/query.png`.

Your task is to:
1. Extract the Cypher query text from the image `/app/query.png` (you can use `tesseract` or similar tools).
2. Write a highly efficient C program at `/home/user/projector.c` that implements this exact graph projection logic.
3. Compile the C program to an executable located at `/home/user/projector`.

**Program Specifications:**
- **Input:** Your program will read a stream of directed edges from `stdin`. The stream consists of whitespace-separated pairs of integers representing `SOURCE_NODE_ID DESTINATION_NODE_ID`. For example: `10 25 \n 25 30`. An `EOF` signals the end of the input graph. 
- **Processing:** Build an in-memory graph from these edges, and execute the projection logic defined in the extracted Cypher query.
- **Output:** Print the resulting node pairs as comma-separated values to `stdout`, one pair per line (e.g., `10,30`).
- **Ordering:** The output lines must be sorted numerically by the first node ID, and then by the second node ID in ascending order. Do not output duplicate pairs.

Ensure your code handles cyclic graphs safely and processes up to 10,000 edges efficiently. The automated test suite will rigorously test your executable against a reference oracle with randomized graphs to ensure bit-exact equivalence.