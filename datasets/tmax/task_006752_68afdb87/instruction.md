I am a researcher organizing my dataset of academic publications. I have a SQLite database located at `/home/user/research.db` that contains tables relating authors and the papers they have published, but the original schema documentation was lost. 

Your task is to:
1. Reverse engineer the relational data model in `/home/user/research.db` to understand how authors and papers are linked.
2. Map this relational data into a co-authorship knowledge graph pattern. In this graph, an "edge" exists between two authors if they have co-authored at least one paper together.
3. Write and execute a Python script to find the author who has the highest number of *unique* co-authors (degree centrality).
4. Output your final finding in a JSON file at `/home/user/result.json` with the exact following format:
```json
{
  "top_author": "Author Name",
  "coauthor_count": <integer>
}
```

Please ensure the JSON file is valid and contains only the specified keys.