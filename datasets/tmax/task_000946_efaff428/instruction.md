You are assisting a researcher who is organizing a newly acquired academic dataset. You have been provided with a SQLite database located at `/home/user/research_data.sqlite`. The database contains information about research papers, authors, and a citation network. 

The researcher doesn't know the exact schema of the database and needs you to perform a series of analytical tasks to summarize the data. 

Please perform the following steps:

1. **Schema Mapping:** Inspect the SQLite database and extract the `CREATE TABLE` statements for all tables. Save this output exactly as it appears in the database to `/home/user/schema_info.txt`.

2. **Recursive Citation Network:** The researcher wants to know the maximum depth of the citation chain starting from the paper with `id = 10`. A citation chain depth is defined as the number of edges in the longest path of citations (where paper 10 cites paper A, which cites paper B, etc.). 
   Write a query using a Recursive CTE to calculate the maximum citation depth starting from paper `10`. Save the resulting integer (just the number) to `/home/user/longest_chain.txt`.

3. **Window Functions & Aggregation:** The researcher wants to find the top 2 authors for each publication year, ranked by the total number of citations their papers (published in that specific year) have received across the entire dataset. 
   - Calculate the total citations received by each paper.
   - Sum these citations per author, per year of publication.
   - Use a window function to rank the authors within each year based on this total citation count (descending order). If there is a tie, order by the author's name alphabetically (ascending).
   - Filter to keep only the top 2 ranked authors per year.
   - Save the results to `/home/user/top_authors.csv` with the exact header: `Year,AuthorName,TotalCitations,Rank`.

You can use Python, bash, or the `sqlite3` CLI to complete these tasks.