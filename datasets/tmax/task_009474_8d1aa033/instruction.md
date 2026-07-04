You are an AI assistant helping a network researcher organize and analyze a dataset of academic paper citations and author affiliations. The researcher wants to use a NoSQL database to perform complex graph aggregations to determine the "influence metrics" of specific seed papers.

Your task involves setting up the database, loading the data, and writing a Python script to execute a multi-stage aggregation pipeline. 

Here are the specific steps:

1. **Environment Setup:**
   Install a local instance of MongoDB server and the `pymongo` Python driver. Start the MongoDB service in the background (you can use `mongod --dbpath /tmp/mongo --logpath /tmp/mongo.log --fork` after creating the `/tmp/mongo` directory if systemd is not available).

2. **Data Preparation:**
   You have been provided with two files in `/home/user/raw_data/`:
   - `papers.json`: Contains academic papers. Each document has `paper_id`, `title`, `impact_factor`, `cites` (a list of `paper_id`s that this paper cites), and `author_id`.
   - `authors.json`: Contains authors. Each document has `author_id`, `name`, and `institution`.
   *(Note: Assume these files exist. If they don't, you must wait for the setup to complete, but for the sake of this test environment, we will generate them before your run. Read them directly).*
   
   Load this data into a local MongoDB database named `research_db`. Create two collections: `papers` and `authors`.

3. **Graph Aggregation Pipeline:**
   Write a Python script at `/home/user/analyze_graph.py` that connects to the `research_db`. The script must execute a single MongoDB aggregation pipeline on the `papers` collection that does the following:
   - Starts by matching the paper with `paper_id: "P001"`.
   - Uses a graph lookup (NoSQL `$graphLookup`) to recursively find all papers that cite this paper (directly or indirectly) up to a maximum depth of 3. (Hint: if Paper B cites Paper A, B's `cites` array contains A's `paper_id`).
   - For the resulting array of citing papers, chain another aggregation stage to calculate:
     - `total_citing_papers`: The total number of unique papers found in the graph lookup.
     - `total_influence_score`: The sum of the `impact_factor` of all these citing papers.
   - Performs a cross-query lookup (e.g., `$lookup`) to fetch the author details (from the `authors` collection) for the original matched paper ("P001").
   - Projects the final output to exactly match this structure:
     ```json
     {
       "seed_paper": "P001",
       "author_name": "Author Name Here",
       "total_citing_papers": X,
       "total_influence_score": Y.Y
     }
     ```

4. **Execution and Output:**
   Run your script and save the exact resulting JSON object to a file located at `/home/user/influence_metrics.json`. 

Please ensure your script handles the aggregation purely within the database (do not fetch all documents into Python and compute the graph in memory).