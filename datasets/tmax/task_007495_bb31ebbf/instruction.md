You are acting as an AI assistant to a compliance officer auditing an organization's IT infrastructure. 

The security team has provided you with a SQLite database dump at `/home/user/infrastructure.db`. However, they did not provide the schema documentation. You need to reverse engineer the data model and perform a complex access audit.

We are looking for potential indirect access violations. Specifically, we want to identify users who accessed a "jump" system that has a direct network path to a "proxy" system, which in turn has a direct network path to a system classified as 'Restricted' (i.e., exactly a 2-hop path: Accessed System -> Proxy System -> Restricted System).

Your task is to write a Bash script at `/home/user/audit.sh` that extracts this information from the SQLite database.

The Bash script must:
1. Query the database to find all systems that act as the start of a 2-hop directed network path to a 'Restricted' system.
2. Find all access events where users logged into these starting systems.
3. Use a SQL Window Function to calculate the chronological "access rank" for each user on that specific system (e.g., their 1st access, 2nd access, etc., ordered by the event timestamp).
4. Output the results to `/home/user/suspicious_access.csv` in the exact format:
   `username,accessed_hostname,event_time,access_rank`
5. The results in the CSV should be ordered primarily by `username` (ascending), then by `event_time` (ascending). 
6. Include a standard CSV header row.

Constraints & Notes:
- Use only Bash and the `sqlite3` CLI tool.
- You must explore `/home/user/infrastructure.db` to understand the table names, column names, and relationships.
- A 2-hop path means `System A -> System B -> System C`, where C is Restricted. You are finding access events for System A.
- Make sure your script has execute permissions (`chmod +x /home/user/audit.sh`) and runs successfully without manual interaction.