We are migrating our legacy web security log analyzer and WAF component from Python 2 to Python 3. The system relies on a high-performance HTTP parser built as a C extension, a SQLite database for rules, and a multi-stage Bash build orchestration script.

Currently, the service source code is located at `/app/waf-service/`. It consists of:
1. A vendored C-based HTTP parser dependency at `/app/waf-service/vendor/http-parser-ext`.
2. A database schema file `/app/waf-service/db/schema_v1.sql`.
3. A build orchestrator Bash script `/app/waf-service/build.sh`.
4. The main Python 2 server script `/app/waf-service/server.py`.

Your task is to completely migrate this system to Python 3 and get the service running. Specifically:

1. **Vendored Package Fix**: The vendored `http-parser-ext` has a build configuration perturbation. Its `Makefile` is hardcoded to build against Python 2.7. You must fix the `Makefile` and `setup.py` (if necessary) so it compiles successfully as a Python 3 extension.
2. **Build Orchestration**: Update the Bash build orchestrator `/app/waf-service/build.sh` to use Python 3 commands (`python3`, `pip3`, etc.) instead of Python 2. Run the script to build and install the vendored parser.
3. **Schema Migration**: Our security rules database must be migrated to a new format. Write a Bash script `/app/waf-service/migrate_db.sh` that reads `/app/waf-service/db/schema_v1.sql`, applies it to a new SQLite database at `/app/waf-service/db/rules.db`, and then executes an `ALTER TABLE` SQL command to add a `rule_hash` (TEXT) column to the `signatures` table.
4. **Python 3 Migration & State Machine**: The `server.py` file contains legacy Python 2 code (using `print` statements, old `urllib2` imports, and `dict.iteritems()`). It implements a simple state machine that reads HTTP requests using the C extension. Refactor `/app/waf-service/server.py` to be fully Python 3 compatible.
5. **Start the Service**: Run the updated `server.py`. It must listen for incoming HTTP traffic on `127.0.0.1:8443`. It should accept a basic `GET /` request and return a `200 OK` response with the body `WAF Active`. Ensure the service remains running in the background.

Please complete all steps and leave the Python 3 HTTP server running on `127.0.0.1:8443`.