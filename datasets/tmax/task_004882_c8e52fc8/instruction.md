You are a cloud architect migrating a legacy interactive data system to a modern REST API architecture. We have two main components located in `/app/`:

1.  **Legacy Interactive Data CLI (`/app/legacy_cli.py`)**: This is a mock interactive system that prompts for a username and password before allowing queries. It reads its data from `/home/user/data_mount/`.
2.  **Modern API Gateway (`/app/api_gateway.py`)**: A skeleton Flask application that needs to expose the legacy data over HTTP.

Your task is to integrate these services:

1.  **Storage Setup**: Create the directory `/home/user/data_mount/`. Inside it, create a file named `config.json` with the following content: `{"status": "migrated", "version": "1.0"}`. (This simulates our newly mounted storage).
2.  **Expect Scripting**: Write a Python adapter module at `/app/adapter.py` that uses the `pexpect` library to interact with `/app/legacy_cli.py`. The legacy CLI expects the username `admin` and the password `supersecret`. It then accepts a `QUERY` command to read a file from the data mount. Your adapter should successfully log in, send the query for `/home/user/data_mount/config.json`, and return the parsed JSON result.
3.  **API Integration**: Modify `/app/api_gateway.py` to import and use your adapter. The Flask app must:
    *   Listen on `127.0.0.1:5000`.
    *   Expose a `GET /api/v1/data` endpoint.
    *   Require an `Authorization: Bearer migrate-token-99` header. If missing or incorrect, return a 401 status code.
    *   On a valid request, use the adapter to fetch the data from the legacy CLI and return it as a JSON response: `{"source": "legacy", "data": {"status": "migrated", "version": "1.0"}}`.
4.  **Startup**: Create a shell script at `/home/user/start_services.sh` that launches the Flask application in the background and saves its PID to `/home/user/api.pid`.

Ensure your adapter correctly handles the interactive prompts of the legacy CLI. The automated verifier will execute your startup script and send real HTTP requests to your API gateway.