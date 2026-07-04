You are an AI assistant helping a researcher organize their dataset. The researcher has a bipartite graph dataset representing authors and the papers they have collaborated on. They need you to process this data to find the most collaborative authors.

The dataset is located in `/home/user/dataset/` and consists of two CSV files:
1. `/home/user/dataset/authors.csv` - Contains `author_id,name`
2. `/home/user/dataset/paper_authors.csv` - Contains `paper_id,author_id`

Your task is to write a standard C++ program (saved as `/home/user/process_graph.cpp`) that performs the following steps:
1. **Join & Materialize:** Read the CSV files and project the bipartite graph into an Author-Author co-authorship graph. An undirected edge exists between two authors if they have both co-authored the same paper.
2. **Graph Analytics:** Calculate the "degree centrality" for each author in this projected graph. Here, degree centrality is defined as the number of *unique* co-authors an author has across all their papers.
3. **Format Conversion & Export:** Find the top 3 authors with the highest degree centrality. If there is a tie in centrality, resolve it by sorting the `author_id` in ascending order. Export the result to a JSON file at `/home/user/top_authors.json`.

The JSON file must strictly follow this exact formatting (including whitespace for array elements, though standard minified is also fine if parseable, please stick to the below structure for safety):
```json
[
  {"author_id": 1, "name": "Alice", "centrality": 5},
  {"author_id": 2, "name": "Bob", "centrality": 3},
  {"author_id": 3, "name": "Charlie", "centrality": 3}
]
```

Requirements:
- Only use the C++ standard library (compile with standard `g++`). No external JSON libraries are allowed; you must construct the JSON string manually.
- The C++ program should read from `/home/user/dataset/` and write to `/home/user/top_authors.json`.
- Compile and execute your program to generate the target file.