You are a database administrator tasked with extracting specific management hierarchy data from an undocumented SQLite database located at `/home/user/knowledge_graph.db`.

Your goal is to find the chain of command (reporting path) from the employee named 'Alice Smith' up to 'Zoe Davis'. 

To complete this task, you must:
1. Analyze the SQLite database to reverse engineer its schema and understand how entities and their relationships (specifically reporting structures) are stored. Be aware that some entity details are stored in a structured text format.
2. Write a script (in a language of your choice) that executes a SQL query (or a series of queries) to traverse this knowledge graph and find the exact path of people from Alice Smith to Zoe Davis based on the reporting relationships.
3. Process the results into a JSON array containing just the names of the employees in the path, in order from Alice Smith to Zoe Davis.
4. Save the final JSON array to `/home/user/management_chain.json`.

Ensure your final JSON file exactly matches a flat JSON array of strings, for example: `["Alice Smith", "Person A", "Person B", "Zoe Davis"]`.