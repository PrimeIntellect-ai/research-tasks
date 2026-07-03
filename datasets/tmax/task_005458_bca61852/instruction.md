You are acting as an AI assistant for a bioinformatics researcher. The researcher has inherited an undocumented SQLite database (`/home/user/research_data.db`) containing experimental results. The data is currently in a relational format, but the researcher needs it reorganized into both Document (JSON) and Graph (CSV) formats to feed into downstream analysis pipelines. 

Your task is to write and execute a Python script (`/home/user/process_data.py`) that explores the database, reverse-engineers the relationships between the tables, and exports the data into the requested formats.

Here is what you need to do:

1. **Reverse Engineer the Data Model**: 
   The SQLite database contains three tables representing Subjects, Trials, and Measurements. However, there are no explicit foreign key constraints defined. You must deduce the relationships based on the column names.

2. **Cross-Representation Mapping & Export**:
   Create a directory `/home/user/export/`. Extract the data using Python's `sqlite3` module and map it into two different paradigms:

   **A. Document Representation (Nested JSON):**
   Create a file `/home/user/export/subjects.json`. This should be a JSON array of subject objects. Each subject should have their attributes and a nested list of `trials`. Each trial should contain its attributes and a nested list of `measurements`.
   The JSON keys should exactly match the column names from the database, except for the nested lists which should be named `trials` and `measurements`.

   **B. Graph Representation (Nodes and Edges CSVs):**
   Create two CSV files for a graph database import:
   - `/home/user/export/nodes.csv`: Must have headers `node_id,node_type,label`. 
     - `node_id` must be prefixed to guarantee uniqueness: `sub_<id>`, `trial_<id>`, `meas_<id>`.
     - `node_type` must be one of `Subject`, `Trial`, or `Measurement`.
     - `label` should be the subject's name, the trial's condition, or the measurement's sensor name.
   - `/home/user/export/edges.csv`: Must have headers `source,target,relation`.
     - Edges must point from Subject to Trial (relation: `HAS_TRIAL`) and Trial to Measurement (relation: `HAS_MEASUREMENT`).
     - Use the prefixed `node_id`s for source and target.

Write your script, execute it, and ensure the three output files are generated precisely as specified.