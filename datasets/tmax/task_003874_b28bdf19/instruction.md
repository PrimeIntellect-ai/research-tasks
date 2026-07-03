You are assisting a data researcher in organizing an unstructured dataset into a structured graph database format. 

The researcher has an audio recording of a domain expert dictating a set of organizational relationships (who manages whom, and who works on which projects). The audio file is located at `/app/interview_tape.wav`.

Your task is to:
1. Transcribe the audio file to text. You may install any Python packages you need (e.g., `openai-whisper` or `SpeechRecognition`) to transcribe the audio locally.
2. Parse the transcription to reverse-engineer the underlying data model. The entities are typically "Employees" and "Projects". The relationships are typically "MANAGES" (between two employees) and "WORKS_ON" (between an employee and a project).
3. Design an indexing strategy to ensure fast lookups by Employee name and Project name.
4. Write a Python script located at `/home/user/process_graph.py` that automates this workflow: it should read the audio, transcribe it, parse the relationships, and generate a Cypher query script located at `/home/user/graph_init.cypher`.

The `/home/user/graph_init.cypher` file must contain:
- The Cypher statements to create the necessary indexes for `Employee` (on a `name` property) and `Project` (on a `title` property).
- The Cypher statements to create all the nodes and edges dictated in the audio. Format your data creation strictly as `MERGE (a:Employee {name: "..."})-[:MANAGES]->(b:Employee {name: "..."})` or `MERGE (a:Employee {name: "..."})-[:WORKS_ON]->(b:Project {title: "..."})` to ensure idempotent execution.

Focus heavily on accurately extracting the relationships from the noisy transcription. The automated test will parse your `/home/user/graph_init.cypher` file, extract the relationships you've defined, and calculate an F1 score against the true hidden relationships in the audio.