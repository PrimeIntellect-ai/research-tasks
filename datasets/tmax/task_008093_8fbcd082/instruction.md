You are helping a researcher organize and analyze a bibliometric dataset stored in a local SQLite database (`/home/user/research_data.db`). 

The researcher has written a C++ program (`/home/user/metrics.cpp`) to calculate author citation metrics and output them to a JSON file. However, the program's SQL query is producing massively inflated citation counts due to a classic implicit cross-join bug, and it is missing the required analytical window functions.

Your task has three parts:

**1. Fix the SQL Query in `metrics.cpp`:**
The C++ program currently attempts to find the total citations for each author. You must fix the query to properly join the tables and avoid the cross-join. Furthermore, you must add a window function to the query to calculate each author's `institution_rank`: their rank within their institution based on `total_citations` (highest citations gets rank 1, ties share the rank using standard `RANK()`).

The database schema is:
- `institutions (id INTEGER PRIMARY KEY, name TEXT)`
- `authors (id INTEGER PRIMARY KEY, name TEXT, institution_id INTEGER)`
- `papers (id INTEGER PRIMARY KEY, title TEXT)`
- `authorships (author_id INTEGER, paper_id INTEGER)`
- `citations (citing_paper_id INTEGER, cited_paper_id INTEGER)` 
  *(Note: `cited_paper_id` is the paper receiving the citation).*

**2. Output the Correct JSON Schema:**
Ensure the compiled C++ program writes the results to `/home/user/metrics_output.json`. The output must be a valid JSON array of objects, sorted by `total_citations` descending, then by `author_id` ascending.
Schema for each object:
```json
{
  "author_id": 1,
  "author_name": "Alice Smith",
  "institution_name": "MIT",
  "total_citations": 42,
  "institution_rank": 1
}
```

**3. Generate Graph Database Queries:**
The researcher also wants to migrate the top researchers to a Neo4j database. 
Create a standalone file `/home/user/graph_setup.cypher` containing Cypher queries to create nodes and relationships **only** for authors who achieved an `institution_rank` of exactly 1.
For each such author, write exact Cypher `CREATE` statements to make an `Author` node, an `Institution` node (if it doesn't already exist in the script's logic, using `MERGE` is preferred), and a `WORKS_AT` relationship.
Example format required in the `.cypher` file:
```cypher
MERGE (i:Institution {name: "MIT"})
CREATE (a:Author {name: "Alice Smith", total_citations: 42})
CREATE (a)-[:WORKS_AT]->(i)
```
Separate each author's block with a newline.

**Environment Details:**
- Compile the C++ program using `g++ -std=c++17 /home/user/metrics.cpp -lsqlite3 -o /home/user/metrics`.
- Run it to produce the JSON file.
- `nlohmann/json.hpp` is available at `/usr/include/nlohmann/json.hpp` if you wish to use it in your C++ code.