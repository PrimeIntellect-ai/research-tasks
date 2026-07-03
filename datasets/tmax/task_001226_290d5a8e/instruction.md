You are an AI assistant helping a researcher organize and query their datasets. The researcher has a custom dataset of academic publications, authors, and institutions, but lacks a database engine. They want to process this data using a fast, standalone C program.

The dataset is stored in three tab-separated values (TSV) files located in the `/home/user/data/` directory (these files already exist):
1. `/home/user/data/institutions.tsv` - Columns: `inst_id` (int), `name` (string), `country` (string)
2. `/home/user/data/authors.tsv` - Columns: `author_id` (int), `name` (string), `inst_id` (int)
3. `/home/user/data/publications.tsv` - Columns: `pub_id` (int), `author_id` (int), `title` (string), `year` (int), `citations` (int)

Your task is to write a C program at `/home/user/process_data.c` that acts as a custom query engine. The program must implement the equivalent of the following SQL query using standard C libraries (no external database libraries allowed):

```sql
SELECT i.name, SUM(p.citations) as total_citations
FROM institutions i
JOIN authors a ON i.inst_id = a.inst_id
JOIN publications p ON a.author_id = p.author_id
WHERE i.country = 'Canada' AND p.year > 2010
GROUP BY i.name
ORDER BY total_citations DESC, i.name ASC
LIMIT 3;
```

Requirements:
1. Write the C code in `/home/user/process_data.c`.
2. Compile it using `gcc -O3 /home/user/process_data.c -o /home/user/process_data`.
3. Execute `/home/user/process_data`.
4. The program must write the final output to `/home/user/results.csv`.
5. The output format in `/home/user/results.csv` should be comma-separated values, specifically `Institution Name,Total Citations`, with one record per line and no header row.

Assume standard string lengths (e.g., maximum 255 characters for titles/names) and that the TSV files are properly formatted. Ensure your program handles the data joining and aggregation efficiently in memory.