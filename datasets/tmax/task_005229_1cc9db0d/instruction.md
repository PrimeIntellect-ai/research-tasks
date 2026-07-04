You are a Database Reliability Engineer (DBRE) dealing with a suspected ransomware attack that has corrupted several of our automated backup clusters. 

We have an automated backup system that stores metadata in an SQLite relational database (`/app/metadata.db`) mapping out a dependency graph of our infrastructure. The actual backup records are stored as JSON documents. We suspect the attacker injected corrupted JSON backup records to poison our restoration process.

Before leaving the grid, the lead engineer left a voicemail at `/app/incident_report.wav` detailing how to identify the corrupted records. You will need to transcribe or listen to this audio file to get the exact technical criteria for the corruption signature.

Your task is to:
1. Reverse engineer the data model by inspecting `/app/metadata.db`. It contains a representation of our knowledge graph (nodes and edges).
2. Transcribe `/app/incident_report.wav` to understand the cross-representation mapping rule the lead engineer discovered. The audio explains how a specific mathematical property of the graph in the SQLite database should correspond to a field in the JSON backup documents.
3. Write a Python script at `/home/user/verify_backup.py` that acts as a filter.
   - The script must accept a single command-line argument: the path to a JSON backup file.
   - It must read the JSON file, extract the necessary identifiers, and query the `/app/metadata.db` graph.
   - It must perform the graph analytics/summarization described in the audio to verify the integrity of the JSON file.
   - If the backup is **CLEAN**, the script must exit with status code `0`.
   - If the backup is **CORRUPTED**, the script must exit with status code `1`.

We will test your script against a hidden quarantine zone of clean and malicious files to ensure it perfectly separates them. Ensure your code is robust and efficient.