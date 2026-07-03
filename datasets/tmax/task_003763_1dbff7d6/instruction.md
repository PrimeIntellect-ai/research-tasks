You are assisting a compliance officer who is auditing our graph database infrastructure. Recently, new regulations were enacted regarding our internal Neo4j system. The specifics of these restricted access patterns were distributed in a secure voice memo.

Your tasks are:
1. Locate and transcribe the audio briefing located at `/app/compliance_briefing.wav`. This audio contains the exact name of a banned node label and a banned relationship type that are no longer permitted in our Cypher queries. (You may use tools like `whisper` or `ffmpeg` installed on the system to extract or transcribe the audio).
2. Write a Python script at `/home/user/audit_query.py` that acts as an automated compliance filter for Cypher queries. 
3. The script must accept a single command-line argument: the absolute path to a text file containing a single Cypher query.
4. The script must analyze the Cypher query text. If the query attempts to access the banned node label OR traverse the banned relationship type identified in the audio, the script must print `REJECT` to stdout and exit with status code 1.
5. If the query is fully compliant (does not contain the banned elements), the script must print `ACCEPT` to stdout and exit with status code 0.
6. The matching should be case-sensitive to standard Cypher syntax (e.g., node labels are typically CamelCase, relationship types are typically UPPER_SNAKE_CASE). 

Ensure your Python script is robust. We will automatically test `/home/user/audit_query.py` against a hidden "clean" corpus of permitted queries and an "evil" corpus of non-compliant queries. Your script must perfectly separate them.