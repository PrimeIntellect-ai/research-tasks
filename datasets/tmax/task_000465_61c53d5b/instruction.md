You are assisting a financial compliance officer in auditing an internal transaction routing system. We suspect that some sub-networks are unwittingly facilitating rapid money movement between sanctioned entities through multi-hop obfuscation. 

Your objective is to build a graph analysis detection tool in C that flags non-compliant ("evil") transaction networks versus compliant ("clean") ones.

Step 1: Sanctioned Entity Extraction
An image of the latest restricted entity IDs has been securely provided at `/app/sanction_list.png`. 
- Use OCR (e.g., `tesseract`, which is preinstalled) to extract the text from this image.
- Save the extracted integer IDs to a text file at `/home/user/sanctioned.txt` (one integer ID per line).

Step 2: Detector Implementation
You must write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`. 
The program will be invoked from the command line with two arguments:
`./detector <path_to_transaction_graph.csv> <path_to_sanctioned_entities.txt>`

The transaction graph CSV files have no header and contain rows in the format: `source_node_id,destination_node_id,transaction_amount`. 

Your C program must project this data into a directed in-memory graph. Then, it must compute graph traversals to evaluate the following compliance rule:
**A transaction network is considered "EVIL" (non-compliant) if there is any directed path of 3 hops or fewer from any sanctioned entity to any *other* distinct sanctioned entity.** 

If such a path exists, the program must print exactly `EVIL` to standard output and exit.
If no such path exists, the program must print exactly `CLEAN` to standard output and exit.

Step 3: Validation
To test your implementation, we have provided two directories containing transaction network snapshots:
- `/app/evil/`: Contains CSV files that violate the compliance rule.
- `/app/clean/`: Contains CSV files that strictly adhere to the compliance rule.

Your compiled detector must accurately classify all files in both directories. You should test your program against these files and refine it until it achieves 100% accuracy.

Constraints:
- You must use C as the primary language for the detector.
- Do not use external C graph libraries; implement the graph projection, materialization, and shortest-path/traversal logic (e.g., BFS or DFS) yourself.
- Assume maximum node ID is less than 10,000.