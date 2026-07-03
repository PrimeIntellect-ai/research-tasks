You are a compliance officer auditing a complex corporate network for potential money laundering and hidden ownership. You have been provided with a dataset representing corporate ownership structures.

Your task is to analyze this ownership graph using Python to identify Ultimate Beneficial Owners (UBOs) and locate the central "shell companies" used to obfuscate control.

The dataset is located at `/home/user/ownership.csv`. It has three columns: `source`, `target`, and `weight`. 
- `source` is the ID of the entity that owns shares. Individuals start with `I_` (e.g., `I_1`), and companies start with `C_` (e.g., `C_1`).
- `target` is the ID of the company being owned (always starts with `C_`).
- `weight` is the percentage of ownership (0 to 100).

Your analysis must accomplish the following:

1. **Hierarchical Ownership Resolution (UBO Extraction):**
   Calculate the total (direct + indirect) ownership percentage that each Individual (`I_`) holds in each Company (`C_`). 
   - Indirect ownership is calculated multiplicatively. If A owns 50% of B, and B owns 50% of C, A owns 25% of C. 
   - Where multiple paths exist (e.g., A owns C through B, and also directly), sum the percentages from all paths.
   - A regulatory violation occurs if an Individual holds **strictly more than 25%** (total ownership > 25.0) of any company, but that individual does *not* have a direct edge to that company in the CSV.

2. **Graph Analytics (Intermediary Detection):**
   Treat the `ownership.csv` data as an unweighted, directed graph (edges point from owner to owned). Calculate the **Betweenness Centrality** of all nodes using standard algorithms (you may use the `networkx` library). 
   - Identify the top 2 Companies (`C_` prefix) with the highest betweenness centrality. These are the primary intermediaries. Tie-breaker: sort alphabetically by Company ID.

3. **Output Generation:**
   Create a JSON report at `/home/user/audit_report.json` with the following exact structure:
   ```json
   {
     "hidden_ubos": [
       "I_X owns 38.4% of C_Y",
       "..."
     ],
     "top_intermediaries": [
       "C_A",
       "C_B"
     ]
   }
   ```
   *Note: Format the percentage in `hidden_ubos` to exactly 1 decimal place. The list should be sorted alphabetically by the Individual ID, then by Company ID.*

Write and execute the necessary Python scripts to process the graph and generate the final `audit_report.json`.