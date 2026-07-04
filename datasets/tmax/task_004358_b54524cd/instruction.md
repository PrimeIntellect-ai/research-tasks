You are a database reliability engineer analyzing complex backup dependency chains. Our database backups are structured as a Directed Acyclic Graph (DAG) where some backup jobs depend on the successful completion of others.

We need a Python tool to calculate a "Criticality Score" for each backup job to prioritize resource allocation. We have vendored the `networkx` package for graph analytics, but the installation is currently broken.

Your tasks:
1. **Fix the Vendored Package:**
   We have vendored `networkx-2.8.8` in `/app/networkx`. However, a junior engineer accidentally introduced a syntax error in `/app/networkx/networkx/classes/digraph.py` (around line 20, missing a colon or a typo in an import) that prevents the package from being imported. Find and fix this perturbation so `networkx` is usable. You must use this specific vendored version by ensuring `/app/networkx` is in your Python path.

2. **Write the Backup Path Analyzer:**
   Create a Python script at `/home/user/backup_analyzer.py` that processes a JSON file containing backup job metadata and outputs a CSV with the calculated criticality scores.

   The script will be invoked as:
   `python /home/user/backup_analyzer.py <input_json_path> <output_csv_path>`

   **Input Format:**
   A JSON list of objects, where each object represents a backup job:
   ```json
   [
     {"job_id": "db_auth", "depends_on": [], "duration_minutes": 10},
     {"job_id": "db_users", "depends_on": ["db_auth"], "duration_minutes": 20},
     {"job_id": "db_analytics", "depends_on": ["db_users"], "duration_minutes": 45}
   ]
   ```
   *Dependency direction:* An edge exists from job X to job Y if Y depends on X.

   **Criticality Score Calculation:**
   For each job $N$, the score is calculated as:
   $Score(N) = (\text{Sum of } duration\_minutes \text{ of } N \text{ and all its descendants}) \times (\text{Count of } N \text{ and all its ancestors})$

   **Output Format:**
   A standard CSV file with headers `job_id,criticality_score`.
   The rows MUST be sorted lexicographically by `job_id`.

Your script must be fully self-contained (relying only on standard libraries and the fixed `networkx` package) and strictly adhere to the input/output paths provided via command-line arguments. It will be tested against numerous randomly generated backup topologies to ensure perfect behavioral equivalence with our reference implementation.