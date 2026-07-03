You are an AI assistant helping a researcher organize and analyze a dataset of academic papers. 

The researcher has provided an SQLite database at `/home/user/research_data.db`. You do not know the exact schema, but it contains information about `authors`, `papers`, and `citations`. 

Your task is to write a bash script at `/home/user/analyze.sh` that queries this database using the `sqlite3` command-line tool. The script must execute a single SQLite query (or a pipeline) that does the following:

1. Calculates the total number of citations for each paper.
2. Uses an SQL Window Function to rank the papers for **each author** based on their total citations (highest citations gets rank 1). 
3. Only papers published **after the year 2010** should be included in this ranking and analysis.
4. Filters the results to keep only the **#1 ranked** eligible paper(s) for each author. If there is a tie for the #1 spot for an author, include all tied papers.
5. Sorts the final output globally by `TotalCitations` in descending order. If there is a tie in citations, sort by the paper's title in ascending alphabetical order.
6. Limits the final output to the top 10 rows.

The script must write its final output to `/home/user/top_papers.txt` in the following pipe-separated format:
`AuthorName|PaperTitle|TotalCitations`

Make sure your script is executable and handles the database file correctly.