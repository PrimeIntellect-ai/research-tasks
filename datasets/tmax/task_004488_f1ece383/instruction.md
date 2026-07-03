You are a build engineer managing an artifact registry for an internal CI/CD system. Our legacy system logged artifact webhooks directly into a SQLite database, but we need to migrate this data into a properly structured relational schema.

A SQLite database is located at `/home/user/artifacts.db`. It contains a single table `v1_artifacts` with the following schema:
`CREATE TABLE v1_artifacts (id INTEGER PRIMARY KEY, webhook_url TEXT);`

The `webhook_url` contains routed paths and encoded query parameters in the following format:
`http://build.internal/api/v1/artifacts/<project_name>/<version>?file=<filename>&encoded_meta=<data>`

The `encoded_meta` parameter is a URL-encoded, Base64-encoded string. Once URL-decoded and Base64-decoded, it reveals a comma-separated key-value pair string of metadata (e.g., `branch=main,commit=a3f29cd`).

Your task is to perform a schema migration using a Bash script:
1. Create a new table in `/home/user/artifacts.db` called `v2_artifacts` with the following schema:
   `CREATE TABLE v2_artifacts (id INTEGER PRIMARY KEY, project TEXT, version TEXT, filename TEXT, branch TEXT, commit_hash TEXT);`
2. Write and execute a Bash script (e.g., `/home/user/migrate.sh`) that reads all rows from `v1_artifacts`.
3. For each row, parse the URL to extract the `project_name`, `version`, and `filename`.
4. Extract, URL-decode, and Base64-decode the `encoded_meta` parameter to find the `branch` and `commit` values.
5. Insert the parsed and decoded data into the `v2_artifacts` table, maintaining the original `id`.

Example row in `v1_artifacts`:
`id`: 1
`webhook_url`: `http://build.internal/api/v1/artifacts/frontend/v1.0.0?file=bundle.js&encoded_meta=YnJhbmNoPW1haW4sY29tbWl0PWEzZjI5Y2Q%3D`

Expected resulting row in `v2_artifacts`:
`id`: 1
`project`: frontend
`version`: v1.0.0
`filename`: bundle.js
`branch`: main
`commit_hash`: a3f29cd

Write your script to handle this migration for all rows present in the database. Ensure your script is robust enough to handle the URL routing format correctly. The database already exists and contains the legacy data.