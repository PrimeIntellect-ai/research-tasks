I am a researcher trying to organize a large dataset of academic papers, authors, and funding grants. My lab has decided to transition our relational data mapping logic into a graph database (using Cypher). However, we are running into two major roadblocks. 

First, we are using a specialized local graph querying parser package vendored at `/app/pycypher-ast-1.2.0` to validate our queries. Unfortunately, it fails to parse query parameters correctly when they are nested inside node properties (it throws an unexpected `AST_PARSE_ERROR` when given variables like `$param`). There seems to be a bug or broken regex in the package's parser logic that was introduced recently. I need you to fix the source code of this vendored package and reinstall it so that it correctly parses parameterized queries.

Second, I need a Python script to automatically translate our legacy relational filter schemas into optimized, parameterized Cypher graph queries. 
Create a script at `/home/user/schema_mapper.py`. It should take exactly one command-line argument: a JSON string representing the relational filter. 
The JSON schema looks like this:
```json
{
  "entity": "Paper",
  "filters": {
    "year_published": 2022,
    "author_id": "A123"
  },
  "return_fields": ["title", "doi"]
}
```
Your script must output exactly one string to `stdout`: the equivalent Cypher query parameterized correctly.
For the example above, the exact expected output is:
`MATCH (n:Paper)-[:AUTHORED_BY]->(a:Author {id: $author_id}) WHERE n.year_published = $year_published RETURN n.title, n.doi`

The relationships in our graph are:
- `Paper` to `Author`: `(p:Paper)-[:AUTHORED_BY]->(a:Author)`
- `Paper` to `Grant`: `(p:Paper)-[:FUNDED_BY]->(g:Grant)`
- `Author` to `Institution`: `(a:Author)-[:AFFILIATED_WITH]->(i:Institution)`

The JSON input will specify a root `entity` (either "Paper", "Author", or "Grant"), a `filters` dictionary (keys can be `author_id`, `grant_id`, `institution_id`, or scalar properties of the root entity like `year_published` or `amount`), and `return_fields`. 

Your script must dynamically map relational ID filters (like `author_id`, `grant_id`) into the correct graph path relationships rather than treating them as scalar properties of the root entity. Any non-ID fields in `filters` should be treated as scalar properties of the root entity. You must use parameterized Cypher variables for all filter values (e.g., `$author_id`, `$year_published`).

Requirements:
1. Fix the vendored package at `/app/pycypher-ast-1.2.0` so it accepts the `$` parameter prefix. 
2. Write `/home/user/schema_mapper.py` to output the exact, optimal Cypher query for the inputted JSON constraint. 
3. Ensure all graph queries map IDs to their corresponding connected nodes rather than raw attributes.