You are an AI assistant helping a researcher organize and analyze a messy academic citation dataset.

The researcher has a dataset of paper citations in `/home/user/raw_citations.jsonl`. 
However, the system that exported this dataset had a corrupted indexing mechanism. As a result, the file contains stale and deleted rows. 

Your task is to write a Python script that builds a data pipeline to clean the data, process it using a NoSQL aggregation pipeline, project it into a graph, and calculate author influence.

Here are the requirements for your pipeline:

1. **Environment Setup:** 
   Install `mongomock` and `networkx` via pip. You will use `mongomock` to simulate a MongoDB instance without needing a background daemon.

2. **Data Cleaning (Query-to-Pipeline):**
   Read `/home/user/raw_citations.jsonl`. Each line is a JSON object with keys: `paper_id`, `author`, `cited_author`, `timestamp`, and `is_deleted`.
   Because of the corrupted index export, there are duplicate `paper_id` entries. 
   You must resolve this by keeping only the entry with the *highest* `timestamp` for each `paper_id`. 
   If the latest entry for a `paper_id` has `"is_deleted": true`, discard that paper entirely.

3. **NoSQL Aggregation:**
   Insert the cleaned, valid records into a `mongomock.MongoClient().db.citations` collection.
   Construct and run a MongoDB aggregation pipeline on this collection that:
   - Groups the records by `author` and `cited_author`.
   - Calculates the total number of citations (`weight`) from `author` to `cited_author`.

4. **Graph Projection & Materialization:**
   Take the results of your NoSQL aggregation and project them into a `networkx.DiGraph()` (Directed Graph).
   - Nodes represent authors.
   - Edges are directed from `author` to `cited_author` with a `weight` attribute equal to the aggregated citation count.

5. **Result Processing:**
   Run the NetworkX PageRank algorithm on this graph (use the default parameters: `alpha=0.85`, `weight='weight'`).
   Save the resulting PageRank dictionary exactly as a JSON file to `/home/user/pagerank.json` (keys are author names, values are their PageRank scores).

Ensure your script handles everything end-to-end when executed.