Hello! I'm a researcher organizing a collection of dataset dependencies, and I need your help writing a C program to analyze a graph of these dependencies. 

I have a file at `/home/user/datasets.jsonl` where each line is a JSON object representing a dataset node. The JSON has a NoSQL-style document structure like this:
`{"id": "dataset_A", "domain": "genomics", "dependencies": ["dataset_B", "dataset_C"]}`

I need you to write a C program located at `/home/user/analyze_graph.c` that does the following:
1. **Database Setup**: Creates an in-memory SQLite database (`:memory:`).
2. **Parameterized Loading**: Reads `/home/user/datasets.jsonl` line by line and inserts the raw JSON strings into a table named `nodes` (with a single column `data` of type TEXT or JSON) using parameterized SQL queries (`?` bindings).
3. **NoSQL Aggregation & Graph Analytics**: Uses SQLite's JSON extraction functions (e.g., `json_extract`, `json_each`) to parse the documents, unnest the `dependencies` arrays, and compute the out-degree (number of dependencies) for each dataset node.
4. **Window Functions**: Uses SQL Window Functions (`RANK() OVER ...`) to rank the datasets within their specific `domain` based on their out-degree (highest degree gets rank 1). If there is a tie in out-degree, break the tie by ordering the `id` alphabetically ascending.
5. **Output**: Writes the results to a CSV file at `/home/user/top_datasets.csv`. The CSV should not have a header row. The format for each row must strictly be: `domain,id,out_degree,domain_rank`. Only include nodes that have an out-degree of 1 or more (ignore nodes with empty dependency lists).

You will need to compile your program using standard tools (e.g., `gcc -O3 /home/user/analyze_graph.c -o /home/user/analyze_graph -lsqlite3`) and execute it. 

Please ensure your program properly handles memory and file pointers. The standard `libsqlite3` library is already available in the environment.