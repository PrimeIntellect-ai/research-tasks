You are a build engineer managing a local artifact repository for an internal data processing pipeline. The artifact metadata is stored in an SQLite database, but it needs to be updated to support dependency tracking and checksums. Additionally, you need to set up a local query server with strict rate limiting to prevent abuse by automated build agents.

Complete the following multi-phase task:

**Phase 1: Schema Migration**
An existing SQLite database is located at `/home/user/artifacts.db`. It has a single table:
`CREATE TABLE packages (id INTEGER PRIMARY KEY, name TEXT, version TEXT, path TEXT, active INTEGER);`
Write a Python script to migrate this schema by adding two new columns to the `packages` table: 
- `checksum` (TEXT)
- `dependencies` (TEXT) - this will store a JSON string of dependency names.

**Phase 2: Constraint Satisfaction & Data Processing**
You have a file `/home/user/incoming_artifacts.json` containing a list of new artifacts in JSON format. Each object has `name`, `version`, `path`, `checksum`, and `dependencies` (a list of package names it depends on).
Write a Python script to process this JSON and update the database:
1. Insert all new packages into the database.
2. The pipeline requires exactly one version of each package to be marked as `active=1`, while others must be `active=0`.
3. Resolve the dependencies for the target package named `"DataPipeline"`. You must mark `"DataPipeline"` and all of its recursive dependencies as `active=1`. Ensure that there are no version conflicts (the JSON guarantees only one valid version combination exists for the DataPipeline closure).
4. Set `active=0` for all packages not in this dependency closure.

**Phase 3: Rate-Limited Query Server**
Create and run a Python web server (using Flask, FastAPI, or standard library) on port 8080 that provides an endpoint:
`GET /package?name=<package_name>`
- It must query the database and return a JSON response: `{"name": "<name>", "version": "<version>", "checksum": "<checksum>"}` for the `active=1` version of the requested package.
- **Request Validation & Rate Limiting:** The endpoint must strictly limit requests to **3 requests per minute per IP address**. If a 4th request from the same IP arrives within 60 seconds, it must return an HTTP 429 status code.

**Verification Step:**
Once your server is running in the background, write and execute a Python script that makes 4 consecutive GET requests to `http://localhost:8080/package?name=DataPipeline`.
Write the HTTP status codes of these 4 requests (one per line) to `/home/user/rate_limit_test.log`.

Requirements for success:
- `/home/user/artifacts.db` is properly migrated and populated.
- Only the correct subset of packages are marked `active=1`.
- `/home/user/rate_limit_test.log` exactly contains the four status codes from your test.