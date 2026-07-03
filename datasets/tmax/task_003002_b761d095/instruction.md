You are a Database Reliability Engineer managing backups for our infrastructure knowledge graph. We have a recent SQLite backup located at `/app/backup.sqlite`, but it has been acting up. Our automated queries are failing because of what appears to be a corrupted index returning stale or missing rows.

Additionally, our security team has provided an image at `/app/pattern.png`. This image contains a text description of a specific infrastructure pattern (a sequence of node types) that they suspect is vulnerable.

Your task:
1. Use OCR (e.g., `tesseract`) to extract the text from `/app/pattern.png`. The text describes a path pattern in the form of node types (e.g., `TypeA -> TypeB -> TypeC`).
2. Fix the database index issues in `/app/backup.sqlite` (hint: running `REINDEX` or rebuilding the indexes on the `edges` and `nodes` tables should clear the corruption).
3. Query the database to find the specific path of node names that matches the sequence of node types extracted from the image. The database schema has two tables:
   - `nodes` (id INTEGER, type TEXT, name TEXT)
   - `edges` (source INTEGER, target INTEGER)
4. Write a script (in Bash, Python, or another available language) to start an HTTP server listening on `127.0.0.1:8080`.
5. The server must expose a `GET /pattern` endpoint that returns the discovered path as a JSON object in the exact format: `{"path": ["name1", "name2", "name3"]}`.
6. Leave the server running in the background so our automated verifier can test it.