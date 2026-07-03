You are a data analyst tasked with implementing a new data processing pipeline. Your manager left a voice memo detailing the business logic for the pipeline at `/app/data_request.wav`. 

You must create a Python script at `/home/user/process_graph.py` that implements the exact pipeline described in the audio recording.

System and Execution Details:
- The script `/home/user/process_graph.py` will be executed in an automated testing environment.
- It will receive a single JSON string via **standard input** containing the raw data.
- The JSON will always have two top-level keys: `"users"` and `"transfers"`.
  - `"users"` is a list of objects with `user_id` (string) and `status` (string).
  - `"transfers"` is a list of objects with `source` (string), `target` (string), and `amount` (float).
- The script must load this data into an in-memory SQLite database (`:memory:`), perform the specific SQL joins and filtering described in the audio, construct a graph using `networkx`, compute the requested metric, and print the final result as a JSON string to **standard output**.
- You are free to install any tools necessary (e.g., `ffmpeg`, `whisper`) to transcribe the audio file and understand the requirements.

Ensure your script handles edge cases (like empty query results) gracefully by outputting an empty JSON object `{}`. The final output must be bit-exact to the specification in the voice memo.