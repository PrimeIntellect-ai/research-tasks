You are an integration developer tasked with testing and modernizing an API gateway configuration. The gateway currently stores its routing configuration and validation logic in a legacy SQLite database, but it needs to be migrated to a new JSON-based configuration file.

Unfortunately, the legacy configuration contains a circular dependency that currently prevents the gateway from building. Furthermore, the validation expressions are written in an outdated proprietary query language that must be translated into standard JavaScript arrow functions for the new Node.js-based gateway.

Your task is to analyze the database, resolve the constraints, translate the logic, and output the final migrated configuration.

**Database Schema:**
The database is located at `/home/user/api_db.sqlite` and contains two tables:
1. `routes` (`id` INTEGER PRIMARY KEY, `path` TEXT, `condition` TEXT)
2. `depends_on` (`route_id` INTEGER, `depends_on_id` INTEGER)
   - A row here means `route_id` **depends on** `depends_on_id`. Therefore, `depends_on_id` must be evaluated *before* `route_id`.

**Requirements:**

1. **Constraint Satisfaction (Fixing the Build):**
   There is at least one circular dependency in the `depends_on` table. You must break all cycles to allow for a valid execution order.
   - To break a cycle, you must remove the *minimum* number of dependency rows possible.
   - If there are multiple edges in a cycle that could be removed to break it, you must remove the dependency row where the `route_id` is the **highest numeric value**.

2. **Schema Migration & Topological Sort:**
   Generate the final configuration in `/home/user/migrated_api.json`.
   The output must be a valid JSON array of route objects.
   The routes in the array **must be topologically sorted** based on the corrected dependencies (i.e., a route must appear after all routes it depends on).
   - If multiple routes can be placed in a given position (a tie in the topological ordering), sort them in ascending order of their `id`.

3. **Code Translation & Expression Parsing:**
   Each route object in the exported JSON must have the following keys:
   - `id` (integer)
   - `path` (string)
   - `js_validator` (string)

   The `js_validator` must be a direct translation of the legacy `condition` string into a valid JavaScript arrow function that takes a single argument `req` and returns a boolean.
   **Translation Rules:**
   - The expression should take the form `req => <translated_condition>`
   - `param.X` becomes `req.param.X`
   - `header.X` becomes `req.header.X`
   - `=` becomes `===`
   - `!=` becomes `!==`
   - `AND` becomes `&&`
   - `OR` becomes `||`
   - Assume parenthesis are preserved exactly as they are.
   - Example Legacy: `(param.type = "admin" OR param.type = "superuser") AND header.token != "none"`
   - Example Translated: `req => (req.param.type === "admin" || req.param.type === "superuser") && req.header.token !== "none"`

Create the final JSON file at `/home/user/migrated_api.json`. You may use any language of your choice (Python, Node, Bash, etc.) to accomplish this task.