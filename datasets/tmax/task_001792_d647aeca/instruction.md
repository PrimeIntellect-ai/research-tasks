You are acting as a compliance officer auditing a corporate ownership database. We need to identify potential "circular control" structures—specifically, instances where three corporate entities form a closed loop of ownership, which is a pattern often used to obscure true beneficial ownership (similar to how circular dependencies cause deadlocks in concurrent systems).

You have been provided with a JSON export of the NoSQL ownership database located at `/home/user/ownership_data.json`. 
The file contains a list of documents. Each document represents an entity and contains an `entity_id` and an `owns` array. Each object in the `owns` array has a `target_id` and a `percentage`.

Your task is to write and execute a Python script that analyzes this schema and extracts these circular control structures. 

Specifically, you must:
1. Find all distinct cyclic ownership chains of exactly 3 entities (e.g., A owns B, B owns C, and C owns A).
2. Filter the relationships so that only ownership links with a `percentage >= 25` are considered valid for forming a cycle.
3. Normalize each found cycle by sorting the three `entity_id`s alphabetically (e.g., if the cycle is E3 -> E1 -> E2 -> E3, represent it as `["E1", "E2", "E3"]`).
4. Ensure all distinct cycles are completely unique in your final list.
5. Sort the overall list of normalized cycles lexicographically (ascending order by the first element, then the second, then the third).
6. Apply pagination to the sorted list. Assuming a page size of 5 results per page and that page numbers are 1-indexed, extract ONLY Page 2.
7. Save the resulting JSON array (which should contain the cycles for Page 2) to `/home/user/compliance_report.json`.

Ensure your output in `/home/user/compliance_report.json` is strictly a valid JSON array of lists of strings.