You are assisting a researcher in organizing and analyzing a citation network dataset. 

We have a SQLite database located at `/app/citations.db`. It contains two tables:
1. `papers` (`id` INTEGER PRIMARY KEY, `title` TEXT)
2. `citations` (`source_id` INTEGER, `target_id` INTEGER) - representing a directed graph where `source_id` cites `target_id`.

The researcher left a voice note dictating a specific query they need run on this graph. The voice note is an audio file located at `/app/query.wav`.

Your task is to:
1. Transcribe the audio file `/app/query.wav` to extract the source paper ID and the target paper ID.
2. Write an optimized SQL query (using recursive CTEs) to compute the shortest directed path from the source paper to the target paper in the citation graph.
3. Retrieve the sequence of paper IDs and their corresponding titles along this shortest path.
4. Create a Python HTTP web service that exposes this result. 
   - The service must listen on `127.0.0.1:8080`.
   - It must expose a `GET /citation-path` endpoint.
   - The endpoint must return a JSON response strictly matching this schema:
     ```json
     {
       "source_id": <int>,
       "target_id": <int>,
       "path_length": <int>,
       "path": [
         {"step": 1, "id": <int>, "title": "<string>"},
         {"step": 2, "id": <int>, "title": "<string>"},
         ...
       ]
     }
     ```
   - `path_length` should be the number of edges (number of nodes in path minus 1).

Keep the HTTP service running continuously in the foreground or background once it is ready so that it can be queried.