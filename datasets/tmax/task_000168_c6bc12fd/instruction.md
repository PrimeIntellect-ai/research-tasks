Wake up, you're on call! It's 3:00 AM and our core VideoIndexer service just crashed hard, taking the database down with it. We need you to figure out what happened, recover the data, fix the bug, and get the service back online.

Here is the situation:
We process incoming video streams, extract frame metadata, and save it to an SQLite database. The service crashed while processing `/app/crash_evidence.mp4`. 

You have the following artifacts to investigate:
1. `/app/logs/service.log`: Contains the traceback of the crash.
2. `/app/db/indexer.db` and `/app/db/indexer.db-wal`: The corrupted SQLite database and its Write-Ahead Log. The WAL contains the uncommitted entries right before the crash.
3. `/app/src/server.py`: The Python (Flask/FastAPI) web service source code.
4. `/app/crash_evidence.mp4`: The video file being processed when the crash occurred.

Your objectives:
1. **Database Recovery**: Recover the SQLite database from the corrupted `.db` and `.db-wal` files into a consistent state at `/home/user/recovered.db`. Make sure all partially committed records from the WAL are salvaged.
2. **Traceback Analysis & Bug Fix**: Analyze the traceback in `/app/logs/service.log` to determine why the crash occurred. It was likely a malformed query or race condition related to a specific frame's metadata. Fix the bug in `/app/src/server.py`.
3. **MRE Creation**: Create a Minimal Reproducible Example script at `/home/user/mre.py` that, when run, demonstrates the exact query bug isolated from the web server. It should attempt the exact database operation that failed on a fresh SQLite database (`/home/user/test.db`), causing the original exception to be caught and printed.
4. **Service Restoration**: Update `/app/src/server.py` to point to the newly recovered database (`/home/user/recovered.db`) instead of the corrupted one. Start the web service. It MUST listen on `127.0.0.1:8080`.

The automated verifier will:
- Check that the recovered database exists and contains the salvaged rows.
- Run your `/home/user/mre.py` to ensure it reproduces the underlying issue.
- Issue HTTP requests to your running service on `127.0.0.1:8080` (e.g., `GET /health`, `GET /api/frames/count`) to verify the service is healthy, the bug is resolved, and the recovered data is accessible.

Good luck! We need this up before the morning traffic spike.