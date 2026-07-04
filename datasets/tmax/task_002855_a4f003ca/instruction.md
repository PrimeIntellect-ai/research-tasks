You are taking over as the Lead Database Administrator for a large financial technology company. Your predecessor left abruptly due to an ongoing issue with MongoDB concurrent transaction deadlocks.

They left a single physical note on their desk which has been scanned and saved to the server at `/app/db_schema_notes.png`. You will need to extract the information from this image (you can use `tesseract` which is pre-installed) to understand the NoSQL data model, the index strategy, and the exact root cause of the deadlocks occurring during aggregation pipeline executions.

Your task is to write a Python script that acts as an automated query validator. It must analyze incoming NoSQL aggregation pipelines and filter out the "deadlock-prone" queries based on the rules reverse-engineered from the scanned note.

Create a Python script at `/home/user/analyze_pipelines.py`.
The script must have the following CLI signature:
`python3 /home/user/analyze_pipelines.py <input.json> <output.json>`

- `<input.json>` will contain a JSON array of MongoDB aggregation pipelines. Each pipeline is itself an array of JSON objects representing pipeline stages (e.g., `{"$match": {...}}`, `{"$lookup": {...}}`, `{"$merge": {...}}`).
- Your script must parse this file, analyze each pipeline, and determine if it is safe to execute or if it violates the deadlock avoidance rules outlined in the image.
- The script must write a JSON array to `<output.json>` containing *only* the pipelines that are perfectly safe (i.e., you must preserve the clean pipelines exactly as they are and drop the evil/deadlock-prone pipelines entirely).

Ensure your script handles complex NoSQL query structures (e.g., checking for the presence and exact order of specific operators and fields as mandated by the index strategy shown in the image).