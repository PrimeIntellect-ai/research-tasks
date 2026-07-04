You are an AI assistant helping a researcher process and cross-reference multiple datasets. 

The researcher has three datasets representing academic publications, each in a different format:
1. `/home/user/authors.csv`: A relational-style CSV file with columns `author_id,name`.
2. `/home/user/papers.jsonl`: A document-style JSON Lines file where each line is a JSON object representing a paper, with keys `id` (string), `year` (integer), and `authors` (a list of integer `author_id`s).
3. `/home/user/citations.txt`: A graph-style edge list of citations. Each line contains two space-separated paper IDs: `citing_paper_id cited_paper_id`.

**Your Task:**
Write a Python script at `/home/user/process_data.py` that processes these files to answer the following query:
Find the total number of valid citations each author has received.
A citation is **valid** if and only if:
- The *cited* paper was published **before 2020**.
- The *citing* paper was published **in or after 2022**.

If a paper has multiple authors, all authors of that paper receive the citation count.

The script must write the results to `/home/user/top_authors.txt`.
The output format must be `Name:Count`, one author per line.
Sort the output first by the citation `Count` in descending order, and then alphabetically by `Name` in ascending order.
Only include authors who have at least 1 valid citation.

You may only use Python's standard library (e.g., `json`, `csv`, `sqlite3` if you choose to build an in-memory database, though it is not strictly required). Run the script to produce the output file.