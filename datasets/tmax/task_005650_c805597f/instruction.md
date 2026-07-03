You are an AI assistant helping a researcher organize and analyze a multi-modal dataset of academic papers. The researcher has provided three files representing different data structures:

1. A relational CSV file at `/home/user/metadata.csv` with the columns `paper_id,year,author`.
2. A graph edge list at `/home/user/citations.txt` where each line contains two space-separated IDs: `source_paper_id target_paper_id` (meaning the source paper cites the target paper).
3. A document JSON file at `/home/user/documents.json` containing a list of objects, each with a `paper_id` and a list of `keywords`.

Your task is to write a Bash script or use a pipeline of shell commands to perform the following cross-representation pattern matching and aggregation:

1. Identify all papers that were published in the year `2022` (based on `metadata.csv`).
2. Filter this subset to find only the papers that cite the paper with ID `P001` (based on `citations.txt`).
3. For these resulting citing papers, extract their `keywords` from `documents.json`.
4. Aggregate these keywords to count the total occurrences of each keyword across this specific subset of papers.
5. Save the final summary in a file located at `/home/user/keyword_summary.txt`. 

The format of `/home/user/keyword_summary.txt` must be a list of the keywords and their counts, sorted first by count in descending order, and then alphabetically by the keyword for ties. Each line should be formatted exactly as `[count] [keyword]`.

Example output format:
3 NLP
2 Graph
1 Ethics
1 Transformers