You are a data engineer tasked with migrating a legacy dependency graph into a modern graph database and exposing it via an internal API. 

We have a legacy system export provided as an image at `/app/legacy_export.png`. 

Your objectives are:
1. **Data Extraction**: Extract the plain text from `/app/legacy_export.png`. The image contains lines defining `Node` entities and `Edge` relationships. `tesseract` is available on the system.
2. **Graph Materialization**: Use Python to create a local, embedded graph database in the directory `/home/user/graph_db`. You must use `kuzu` (pip installable) as the database.
   - Parse the extracted text.
   - Create the appropriate Node tables and Rel (relationship) tables based on the extracted entities.
   - Insert the extracted records into the database. You must use **parameterized queries** for all insertions to prevent injection and optimize the query plan.
3. **Query Optimization**: Create an index on the primary identifier property of each Node table to ensure optimal query execution plans.
4. **Data Retrieval Service (API)**: Build and run a Python web service (e.g., using `FastAPI` or `Flask`) that listens on `127.0.0.1:8080`.
   - Implement a `POST /query` endpoint.
   - The endpoint must accept a JSON payload: `{"employee_id": "<ID>"}`.
   - The endpoint must execute a Cypher query against the Kùzu database to find all Projects the specified Employee works on.
   - It must return a JSON response in the format: `{"projects": ["Project Name 1", "Project Name 2"]}`.

Ensure your service is actively running in the background and listening on port 8080. Write a log file at `/home/user/api.log` capturing the startup of your server. All dependencies can be installed in the default Python environment or a venv.