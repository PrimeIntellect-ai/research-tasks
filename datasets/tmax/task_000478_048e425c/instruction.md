As a Database Reliability Engineer, you need to manage a complex migration and backup validation process for our internal network topology system. 

We are moving from a legacy relational format to a graph-based structure. You must build a unified pathing validator and a backup sanitiser.

Here are your objectives:

1. **Schema Extraction (Image Fixture):** 
There is an architecture diagram at `/app/legacy_schema.png`. You must use OCR or vision processing to read the image and extract the hidden root node identifier and the exact column mapping required to reconstruct the graph from the relational database dumps. 

2. **Cross-Representation Mapping & Shortest Path:**
We have legacy network backups in `/app/data/relational/` (CSV) and document backups in `/app/data/document/` (JSON). Using the schema extracted in Step 1, write a multi-language tool (Python or Ruby is fine) that merges these formats into an in-memory graph. You must compute the shortest path from the extracted root node to the target node `NODE_OMEGA`. Output the shortest path as a comma-separated string to `/home/user/shortest_path.txt`.

3. **Backup Sanitisation (Adversarial Corpus):**
Some backup files have been corrupted with malicious loop-injection nodes designed to break our graph traversals. You must write a sanitiser script (`/home/user/sanitiser.py` or `.rb` or `.js`) that takes an input file path and standardizes/filters the backup data. 
We will test your sanitiser against two corpora:
- A clean corpus of valid backup files.
- An evil corpus of backups containing malicious loop-injection nodes.
Your script should take an input file path as the first argument, and write the sanitised output to standard out. If a file is entirely malicious/invalid, exit with code 1.

Build the sanitiser and run your pathfinding. Ensure all outputs are placed exactly where requested.