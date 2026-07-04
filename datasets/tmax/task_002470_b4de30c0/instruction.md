You are a data engineer building an ETL pipeline that translates semi-structured document data into a flattened knowledge graph format. We have a custom ETL package that handles cross-representation mapping and NoSQL-style aggregation in memory, but it has a bug, and your pipeline needs to achieve a high accuracy metric.

Here is your objective:

1. **Fix the Vendored Package:**
   We are using a proprietary lightweight library called `pygraph_etl` (version 1.2.0) vendored at `/app/pygraph_etl-1.2.0/`. It provides tools for mapping nested JSON documents into a graph schema. However, it contains a bug in its aggregation pipeline logic (specifically in `pygraph_etl/mapper.py`): it fails to properly expand nested arrays when evaluating `has_many` relationships, resulting in missing edges in the output. You need to inspect the source code, identify the perturbation, and patch it so that all edges are generated correctly.

2. **Build the ETL Pipeline:**
   Write a Python script at `/home/user/build_graph.py`. Your script should:
   - Import the fixed `pygraph_etl` package (you may need to install it locally or set `PYTHONPATH`).
   - Read a JSONL dataset located at `/home/user/data/entities.jsonl`. This dataset contains documents with nested relational data (e.g., a "Company" document containing a list of "Employee" objects, which in turn have "Project" IDs).
   - Use the package's `GraphProjector` class to define a schema mapping that extracts three types of nodes (Company, Employee, Project) and two types of edges (`EMPLOYS` between Company and Employee, and `WORKS_ON` between Employee and Project).
   - Materialize the graph and export it to a CSV file at `/home/user/projected_edges.csv`. The CSV must have exactly three columns: `source_id`, `target_id`, and `edge_type` (with a header row).

Your final materialized graph will be tested for completeness. We will compute the Jaccard similarity between your `/home/user/projected_edges.csv` and a hidden ground-truth edge list. You must achieve a similarity score of >= 0.99. 

Do not rely on external services; everything you need is available locally.