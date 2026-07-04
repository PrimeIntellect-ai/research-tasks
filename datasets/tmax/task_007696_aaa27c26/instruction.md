I am a researcher organizing my dataset of academic publications, authors, and co-authorships. I have an SQLite database located at `/home/user/research_data.db`. 

I was trying to extract a list of all co-authorships to build an influence graph. I wrote a SQL query to get pairs of authors who worked on the same paper, but my script froze. I suspect my query has an implicit cross-join that is generating a massive Cartesian product instead of accurately joining the tables based on their relationships.

Here is what you need to do:
1. **Schema Analysis**: Inspect the schema of `/home/user/research_data.db` to understand how papers, authors, and their relationships are stored.
2. **Fix and Export**: Write a corrected SQL query that retrieves legitimate co-author pairs (two different authors who share the same paper). Do not include self-loops (an author co-authoring with themselves), and avoid duplicate pairs if they co-authored multiple papers (treat the graph as unweighted/undirected). Export this edge list to `/home/user/edges.csv` with headers `author1,author2`.
3. **Graph Analytics Pipeline**: Write a Python script to read `/home/user/edges.csv`, construct an undirected graph, and compute the Degree Centrality for every author in the network. 
4. **Format Output**: Extract the top 3 authors with the highest degree centrality. If there are ties, sort them alphabetically by name. Save the final result as a JSON array of objects in `/home/user/top_authors.json` exactly in this format:
```json
[
  {"name": "Author Name", "centrality": 0.85},
  {"name": "Another Name", "centrality": 0.72},
  {"name": "Third Name", "centrality": 0.50}
]
```

Note: You may need to install necessary Python libraries like `networkx` or `pandas` using pip. Ensure your results are exact and properly rounded to 4 decimal places if floating-point precision issues arise, though standard networkx degree centrality output rounded to 4 decimals is expected.