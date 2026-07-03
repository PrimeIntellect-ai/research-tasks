You are assisting a technical writer who is organizing a large documentation repository. We have a live documentation preview stack located in `/app/` that uses a file watcher, a text transformation script, and a web server. 

Currently, the transformation script is broken. It is supposed to handle bulk renaming and macro substitution, but it fails to do so. Your task is to fix the transformation script and bring up the document preview stack so it functions correctly.

Here is the setup:
- `/home/user/docs/src/`: Directory where draft markdown files are written.
- `/home/user/docs/out/`: Directory where processed documentation should be served.
- `/app/watcher.py`: A Python script that watches `/home/user/docs/src/` for file modifications or creations. When a change is detected, it executes `/app/transformer.sh`.
- `/app/transformer.sh`: A broken shell script. It should process all files in `/home/user/docs/src/`, apply macros, and place the results in `/home/user/docs/out/`.
- `/app/server.py`: A Python HTTP server that serves the contents of `/home/user/docs/out/` on `127.0.0.1:8080`.

Your goals:
1. Fix `/app/transformer.sh` (you may use bash, python, perl, etc. within it) so that it performs the following:
   - Copies all files from `/home/user/docs/src/` to `/home/user/docs/out/`.
   - Renames any file starting with `draft_` and ending with `.md` to start with `pub_` and end with `.html`. (e.g., `draft_api.md` becomes `pub_api.html`).
   - Replaces the exact macro `%%STATUS%%` with `PUBLISHED` in all generated files.
   - Replaces the exact macro `%%DATE%%` with `2024` in all generated files.
2. Start the services. You should run `/app/watcher.py` and `/app/server.py` in the background so they are actively listening and processing files.

Ensure the web server is successfully running on `127.0.0.1:8080` and that the file watcher actively responds to new files created in the `src` directory by invoking your fixed transformer. Leave the background processes running when you complete the task.