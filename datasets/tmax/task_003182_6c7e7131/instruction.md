You are assisting a corporate compliance officer auditing a potential insider threat. An intercepted VoIP call was flagged by our data loss prevention system, and we need you to analyze it, correlate it with our access databases, and generate a risk report.

Your tasks are to:

1. **Transcribe the Audio:**
   - The intercepted call is located at `/app/voip_audit.wav`.
   - Install necessary transcription tools (e.g., `openai-whisper`, `ffmpeg`) in your Python environment and transcribe the audio. 
   - Extract two key pieces of information from the audio: the compromised employee's ID (which follows the format `E-XXXX`) and the name of the compromised project they mention.

2. **Hierarchical Database Querying:**
   - We have an access database located at `/app/corp_audit.db` (SQLite3). 
   - The database contains three tables:
     - `employees` (`emp_id` TEXT PRIMARY KEY, `name` TEXT, `manager_id` TEXT)
     - `projects` (`project_name` TEXT PRIMARY KEY, `sensitivity` REAL)
     - `access_logs` (`emp_id` TEXT, `project_name` TEXT, `access_count` INTEGER)
   - Using recursive CTEs or hierarchical queries in Python (`sqlite3`), determine the "peer group" of the compromised employee. The peer group is defined as the compromised employee themselves PLUS all other employees who share the exact same direct `manager_id`.

3. **Cross-Query Aggregation & Risk Scoring:**
   - For this entire peer group, identify all *other* projects they have accessed (do NOT include the compromised project mentioned in the audio).
   - Calculate a "Risk Score" for each of these other projects.
   - The formula for a project's risk score is:
     `Risk Score = (Total access_count by the entire peer group for this project) * (sensitivity of the project)`

4. **Generate the Report:**
   - Create a JSON file at `/home/user/audit_report.json` with the exact following schema:
     ```json
     {
       "compromised_employee": "E-XXXX",
       "compromised_project": "Project Name",
       "risk_scores": {
         "OtherProjectA": 12.5,
         "OtherProjectB": 45.0
       }
     }
     ```

Make sure your risk scores are calculated accurately based on the database joins. Your final JSON file will be graded by an automated verifier against the true expected risk scores.