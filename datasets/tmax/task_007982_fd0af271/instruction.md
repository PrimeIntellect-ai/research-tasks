You are an infrastructure engineer setting up a new polyglot build system. As part of this, you need to migrate an old build database, write a manifest transformer, and set up a rate-limited reverse proxy for build triggers. 

Perform the following tasks using Bash and standard Linux tools (like `jq`, `sqlite3`, `nginx`).

**Part 1: Schema Migration**
You have an existing SQLite3 database at `/home/user/builds.db` containing a table:
`legacy_builds(id INTEGER PRIMARY KEY, repository TEXT, build_data TEXT)`
The `build_data` column contains a JSON string with the schema: `{"lang": "...", "command": "...", "timeout": 120}`.
Write and execute a Bash script at `/home/user/migrate.sh` that migrates this data to a new table:
`active_builds(id INTEGER PRIMARY KEY, repository TEXT, lang TEXT, build_cmd TEXT)`
1. The script must create the new table.
2. It must extract the `lang` and `command` values from the JSON in `build_data` and map them to `lang` and `build_cmd` in `active_builds`.
3. It must copy all records accurately.
4. It must drop the `legacy_builds` table after the migration is complete.

**Part 2: Structured Data Transformation**
Build configurations are provided as JSON files. Write a Bash script at `/home/user/generate_env.sh` that takes a single file path as an argument. 
The input JSON will look like this:
```json
{
  "project": "example",
  "env": {
    "NODE_ENV": "production",
    "PORT": "3000",
    "API_KEY": "secret123"
  }
}
```
The script must parse the `env` object and print to standard output (stdout) the key-value pairs in the format `export KEY="VALUE"`. The output must be sorted alphabetically by the key. If the `env` object is missing or empty, output nothing.

**Part 3: Reverse Proxy & Rate Limiting**
Configure Nginx to act as the trigger endpoint. Create a complete, standalone Nginx configuration file at `/home/user/nginx.conf` that can be run as the standard `user` without root privileges.
Requirements for `/home/user/nginx.conf`:
1. Run in the foreground or background (your choice), but do not use privileged ports or directories. Store the PID file at `/home/user/nginx.pid` and logs at `/home/user/error.log` and `/home/user/access.log`.
2. Configure an `http` block with a server listening on port `8080`.
3. Create a location `/trigger` that proxies requests to `http://127.0.0.1:9999`.
4. Implement rate limiting on the `/trigger` location. Allow exactly 2 requests per minute. Define a `limit_req_zone` named `build_zone` of size `1m` keyed by the client's IP address. Apply it to the location without any `burst` or `nodelay`.
5. Add a custom HTTP response header `X-Build-Proxy: active` to all responses from the port 8080 server.

Once the file is written, start Nginx using:
`nginx -c /home/user/nginx.conf`
Make sure it is running and bound to port 8080 before completing the task.