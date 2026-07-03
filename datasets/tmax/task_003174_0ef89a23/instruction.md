You are acting as a Data Security Analyst. We have recently discovered a security breach and a potential insider threat. The incident response team has left an audio briefing for you at `/app/instructions.wav`. 

Your task is to build a classification tool to filter our incoming support tickets. 

You have access to the following data sources:
1. `/app/employees.csv`: A relational dataset containing `emp_id`, `name`, `manager_id`, and `department`.
2. A set of NoSQL document dumps (JSON format) representing support tickets.

You must build a Python script at `/home/user/classifier.py` that takes two arguments: an input directory containing JSON ticket files, and an output CSV file path.
Usage: `python3 /home/user/classifier.py <input_directory> <output.csv>`

The script must evaluate every `.json` file in the `<input_directory>`. 
The output CSV must contain exactly two columns: `filename` (just the base name of the file, e.g., `ticket_001.json`) and `status` (must be either `clean` or `evil`).

To determine what makes a ticket "evil", you must:
1. Transcribe and listen to the instructions in `/app/instructions.wav`. The audio will specify a compromised manager's ID and specific malicious NoSQL aggregation operators used by the attackers.
2. Perform a recursive/hierarchical query on `/app/employees.csv` to find all employees who report to the compromised manager, either directly or indirectly (any level deep in the hierarchy).
3. Cross-reference the document-based tickets with your relational hierarchy. Flag a ticket as `evil` if:
   a) The `author_id` in the ticket belongs to the compromised manager or any of their direct/indirect subordinates.
   b) The ticket's `query_payload` object contains any of the malicious NoSQL operators mentioned in the audio (e.g., as keys in the JSON structure).
4. If neither condition is met, the ticket is `clean`.

To ensure your tool is robust, we have provided two test corpora:
- `/app/corpus/clean/`: Contains only safe tickets.
- `/app/corpus/evil/`: Contains tickets that must be flagged as evil.

You must ensure your script perfectly separates the clean corpus from the evil corpus. Write the code, test it against both directories, and ensure the logic is fully automated. You may use standard Python libraries or install any transcription tools (like `whisper` or `ffmpeg`) needed to extract the instructions from the audio.