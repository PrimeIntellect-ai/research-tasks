You are an AI assistant helping a researcher organize and query a complex academic dataset. 

The researcher has an SQLite database located at `/home/user/dataset.db` containing academic papers, authors, and citation networks. The database schema uses a mix of relational and document representations:

1. `authors`: `auth_id` (TEXT), `name` (TEXT)
2. `documents`: `doc_id` (TEXT), `metadata` (TEXT) - The `metadata` column stores a JSON object with the format: `{"year": YYYY, "authors": ["auth_id1", "auth_id2", ...]}`
3. `citations`: `source_doc` (TEXT), `target_doc` (TEXT) - A directed graph representation where `source_doc` cites `target_doc`.

**Your Task:**
1. Write a C program located at `/home/user/analyze_graph.c` that connects to this SQLite database.
2. The program must execute a query (or a series of operations) to identify all pairs of authors (Author A, Author B) where Author A has cited Author B **at least 2 times** across the dataset. 
   - A citation from Author A to Author B occurs when a document co-authored by Author A cites a document co-authored by Author B.
   - If Author A and Author B co-author the *same* citing paper, and it cites a paper by Author B, that counts as 1 citation.
   - Self-citations (where Author A cites themselves) should be excluded from the final results.
3. The C program must export the results to `/home/user/frequent_citations.csv`.
4. The output CSV must have exactly this header: `Citing_Author_Name,Cited_Author_Name,Citation_Count`
5. The CSV rows must be sorted by `Citation_Count` in descending order. If there is a tie, sort by `Citing_Author_Name` ascending, then `Cited_Author_Name` ascending.
6. Compile your C program to `/home/user/analyze_graph` and run it to produce the final CSV.

You will likely need to utilize SQLite's JSON functions (`json_each`, `json_extract`) and design an efficient CTE or subquery strategy to bridge the document-relational-graph gap. 

Ensure the final CSV strictly matches the requested format.