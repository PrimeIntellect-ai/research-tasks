You are an AI assistant helping a researcher organize and process their academic datasets. 

The researcher has compiled a SQLite database located at `/home/user/research_data.db`. The database contains a hierarchical taxonomy of research topics and a collection of research papers with their citation counts (acting as a basic measure of graph centrality/influence).

The database has two tables:
1. `taxonomy`: 
   - `id` (INTEGER PRIMARY KEY)
   - `parent_id` (INTEGER, references `id`, can be NULL for root topics)
   - `name` (TEXT)
2. `papers`: 
   - `id` (INTEGER PRIMARY KEY)
   - `topic_id` (INTEGER, references `taxonomy(id)`)
   - `title` (TEXT)
   - `citations` (INTEGER)

Your task is to write a Python script at `/home/user/process_results.py` that processes this dataset using advanced SQL queries via the built-in `sqlite3` module. 

The script must:
1. Use a **Recursive Common Table Expression (CTE)** to find the topic named 'Artificial Intelligence' and all of its descendants in the taxonomy hierarchy.
2. For the resulting topics, calculate the total number of citations across all papers in each topic.
3. Use a **Window Function** to rank the papers within each topic by their `citations` in descending order.
4. Filter the results to only include the top-ranked paper (rank 1) for each topic. If there's a tie, SQLite's default stable sorting is fine, but assume no ties for the top paper.
5. Export the final aggregated and ranked results to a CSV file at `/home/user/top_research.csv`.

The output CSV must have exactly the following header and columns:
`TopicName,TopPaperTitle,TopPaperCitations,TopicTotalCitations`

Sort the output CSV rows alphabetically by `TopicName`.

Do not use external libraries (like pandas or SQLAlchemy); use only Python's standard library (`sqlite3`, `csv`, etc.). Execute your script to generate the output CSV.