You are an AI assistant helping a researcher organize their datasets and automate data retrieval based on voice dictations. 

You have access to a voice dictation from the researcher, stored as an audio file at `/app/dictation.wav`. 
You also have access to a local SQLite database at `/app/knowledge.db` which acts as a relational knowledge graph of the research organization.

The database schema is as follows:
- `researchers` (id INTEGER PRIMARY KEY, name TEXT, specialization TEXT)
- `facilities` (id INTEGER PRIMARY KEY, city TEXT, country TEXT)
- `projects` (id INTEGER PRIMARY KEY, title TEXT, budget REAL)
- `researcher_project` (researcher_id INTEGER, project_id INTEGER)
- `facility_project` (facility_id INTEGER, project_id INTEGER)

Your task is to:
1. Transcribe the audio file located at `/app/dictation.wav`. The audio contains a structured request exactly in the format: `Subject: [Firstname Lastname]. Location: [City].` (for example, "Subject: John Doe. Location: Paris."). You may install and use any Python speech recognition libraries (like `SpeechRecognition` with `pocketsphinx` or `openai-whisper`) to extract this text.
2. Parse the extracted name and city from the transcript.
3. Write a Python script to connect to `/app/knowledge.db` and use parameterized queries, complex joins, and cross-query aggregation to find all `projects` (specifically the `title` and `budget`) that are associated with BOTH the transcribed researcher and the transcribed facility.
4. Calculate the sum of the budgets for these overlapping projects.
5. Expose this result by creating a Python HTTP server that listens on `127.0.0.1:8080`.
6. The server must implement a `GET /api/result` endpoint that returns a JSON response with the following exact structure:
   ```json
   {
     "transcript": "<the exact full text you transcribed>",
     "researcher": "<extracted researcher name>",
     "location": "<extracted city>",
     "projects": ["<Project Title 1>", "<Project Title 2>"],
     "total_budget": <numeric sum of budgets>
   }
   ```
   (Sort the `projects` list alphabetically by title).

Leave the HTTP server running in the background so it can be verified. Ensure all your queries use parameterized inputs to prevent SQL injection, and properly manage database connections.