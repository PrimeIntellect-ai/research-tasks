You are acting as a Database Administrator and Backend Engineer. We have a SQLite database at `/app/company.db` containing an organizational structure. 

The database has two tables:
1. `departments` (has an `id`, `name`, and `parent_id` referencing another department).
2. `employees` (has an `id`, `name`, and `dept_id`).

We need you to build a Python HTTP API that queries this database.

Your requirements:
1. Investigate the database schema.
2. We have a handwritten note from the CTO scanned at `/app/exclude_rule.png`. You must extract the text from this image (using OCR, `tesseract` is installed). It contains a specific `IGNORE_DEPT_ID: <number>`.
3. Create a Python web server (you can use `Flask`, `FastAPI`, or Python's built-in `http.server`) listening exactly on `127.0.0.1:8080`.
4. The server must expose a `GET /hierarchy?dept_id=<id>` endpoint.
5. This endpoint must return a JSON array of `employee` names (just a list of strings, e.g., `["Alice", "Bob"]`) who belong to the specified `dept_id` AND all of its sub-departments recursively.
6. **Crucial Rule**: The hierarchy traversal must COMPLETELY IGNORE the department ID specified in the image and all of its sub-departments.
7. Sort the returned list of employee names alphabetically.
8. The database is large, and your query must be efficient. Please analyze the schema and create any necessary indexes in `/app/company.db` to optimize the recursive and join queries. The API should respond in under 500ms.
9. Keep the server running in the background or foreground so we can test it.

Once your server is running on `127.0.0.1:8080`, simply tell us it's ready.