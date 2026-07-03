You are a data analyst working for a financial intelligence agency. You have been provided with two CSV files representing a simplified corporate knowledge graph containing supply chain and financial data.

The files are located in `/home/user/data/`:
1. `entities.csv`: Contains nodes in the graph.
   Columns: `id,name,type` (Types include 'Company', 'Person', 'Bank')
2. `relationships.csv`: Contains directed edges between nodes.
   Columns: `source,target,relation_type,weight` (Relation types include 'OWNS', 'SUPPLIES', 'LOAN_TO')

Your objective is to analyze this data to find a specific target company. 

Task Requirements:
1. Pattern Matching: Identify all entities of type `Company` that meet BOTH of the following criteria:
   - They receive 'SUPPLIES' from at least two distinct source entities.
   - They are the target of a 'LOAN_TO' relationship from an entity of type `Bank`.
2. Graph Analytics (Centrality): For the subset of companies identified in Step 1, calculate their in-degree centrality specifically for the 'SUPPLIES' relationship (i.e., count the number of incoming 'SUPPLIES' edges).
3. Identify the Primary Target: Find the company from the filtered list with the highest 'SUPPLIES' in-degree count.

You may use any programming language (e.g., Python, bash tools, awk, jq) to complete this task. 

Write your final conclusion to a JSON file at `/home/user/analysis_report.json` with the following exact structure:
```json
{
  "target_company_id": "<ID_HERE>",
  "target_company_name": "<NAME_HERE>",
  "incoming_supplies_count": <INTEGER_COUNT>
}
```
If there is a tie, pick the one that comes first alphabetically by `id`. Make sure to create the `/home/user/data` directory and write your scripts in `/home/user`.