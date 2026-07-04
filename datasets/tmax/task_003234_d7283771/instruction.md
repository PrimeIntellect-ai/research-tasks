You are assisting a compliance officer auditing a massive web of corporate entities. We have a document-oriented dump of the corporate network in `/app/corporate_entities.json`. Each document represents a company and contains its relational links ("owns", "subsidiary_of"), financial metadata, and a "risk_score".

First, you need to listen to the latest audit instructions. The Chief Compliance Officer left an audio memo at `/app/audit_memo.wav`. You will need to transcribe this audio to find the strict compliance rules for this quarter's audit, specifically the risk score threshold. Any corporate entity exceeding this risk score must be completely excluded from the audit paths.

Your objective is to write a Python CLI program at `/home/user/audit_path_finder.py` that dynamically queries this dataset.

Requirements for `/home/user/audit_path_finder.py`:
1. It must accept a single command-line argument: the Target Entity ID (e.g., `CORP-782`).
2. It must load and parse `/app/corporate_entities.json` (cross-representation mapping from document to graph).
3. It must find the shortest path (fewest hops) from the root node `CORP-ROOT` to the provided Target Entity ID.
4. It MUST filter out and completely ignore any nodes that exceed the risk score threshold specified in the audio memo. 
5. It must print ONLY the exact path as a comma-separated list of Entity IDs to standard output. (e.g., `CORP-ROOT,CORP-105,CORP-402,CORP-782`). If no path exists due to the compliance threshold or missing links, print exactly `NO_COMPLIANT_PATH`.
6. The query and graph traversal must be efficient.

Build the script so it can be tested automatically with hundreds of different target IDs. Make sure your final script is located at `/home/user/audit_path_finder.py` and is directly runnable via `python /home/user/audit_path_finder.py <ID>`.