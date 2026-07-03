You are an AI assistant helping a data researcher clean up a massive, multi-modal dataset of academic papers. The researcher has scraped millions of papers, but the dataset is polluted with auto-generated "fake" papers and citation rings.

The infrastructure consists of two cooperating services running locally:
1. **PostgreSQL** (localhost:5432, user: `researcher`, db: `academic_graph`): Contains the relational citation graph. 
   - Table `citations` with columns `source_id` (VARCHAR) and `target_id` (VARCHAR).
2. **MongoDB** (localhost:27017, db: `academic_docs`, collection: `metadata`): Contains the document metadata, including nested JSON structures with authors, affiliations, and full-text abstracts.

Your task is to create a Python-based filter tool that queries these databases to classify papers as either "clean" (legitimate) or "evil" (fake/predatory).

To help you build this classifier, the researcher has provided two training corpora containing plain text files. Each file is named after a `paper_id`:
- Clean examples: `/app/corpus/clean/`
- Evil examples: `/app/corpus/evil/`

You need to reverse-engineer the characteristics of the "evil" papers by analyzing their graph properties in PostgreSQL (e.g., recursive citation loops, isolated clustering, PageRank anomalies) and their document properties in MongoDB (e.g., suspicious metadata patterns).

**Requirements:**
1. Write your solution in `/home/user/paper_filter.py`.
2. The script must accept a single command-line argument: the `paper_id`.
   Example: `python /home/user/paper_filter.py "paper_12345"`
3. The script must query both PostgreSQL and MongoDB to determine the paper's validity.
4. If the paper is legitimate (clean), the script must **exit with code 0**.
5. If the paper is fake/predatory (evil), the script must **exit with code 1**.
6. Do not modify the databases.
7. You may use Python packages like `psycopg2`, `pymongo`, and `networkx`. Install them if necessary.

An automated test will run your script against a hidden holdout set of clean and evil paper IDs. You must achieve 100% accuracy on the verification sets.