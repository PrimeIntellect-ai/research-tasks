You are assisting a technical writer with organizing and securing an automated documentation pipeline. 

The writer's environment runs a multi-service documentation build system located in `/app/`. When the system is started via `/app/start_services.sh`, it spins up the following stack:
1. **Redis** (Port 6379) - Acts as a message queue for file changes.
2. **Watcher** (`/app/watcher.py`) - Monitors the directory `/home/user/docs_src` for changes and pushes the paths of modified files to a Redis list named `doc_queue`.
3. **Builder** (`/app/builder.py`) - Polls `doc_queue`, reads the Markdown files, parses them, and writes the generated HTML to `/home/user/www/`.
4. **Nginx** (Port 8080) - Serves the generated HTML files.

**The Problem:**
The writer frequently receives documentation contributions from external sources. Some of these files contain broken markup, malformed structured data, or malicious include macros that cause the `builder.py` process to crash or, worse, expose system files (e.g., `!INCLUDE[/etc/passwd]`). Since the watcher blindly pushes everything to Redis, the builder is in a constant loop of crashing and restarting.

**Your Tasks:**

1. **Create a Python Sanitizer/Filter:**
   Write a Python script at `/home/user/filter.py` that takes a single file path as a command-line argument. The script must analyze the file and determine if it is "clean" or "evil".
   * **Clean files** must cause the script to exit with code `0`.
   * **Evil files** must cause the script to exit with code `1`.
   
   A file is considered **evil** if it meets ANY of the following criteria:
   * It contains an include macro `!INCLUDE[<path>]` where the path is absolute (starts with `/`) or contains directory traversal (`..`). Safe includes like `!INCLUDE[./other.md]` or `!INCLUDE[images/pic.png]` are allowed.
   * It contains a JSON frontmatter block (content at the very top of the file enclosed by `---` on separate lines) that is syntactically invalid JSON.

2. **Validate against the Corpora:**
   To test your filter, you have been provided with two directories:
   * `/home/user/corpora/clean/` - Contains 50 valid, safe markdown files.
   * `/home/user/corpora/evil/` - Contains 50 malformed or malicious markdown files.
   Your `/home/user/filter.py` MUST reject 100% of the evil corpus and accept 100% of the clean corpus.

3. **Integrate with the Pipeline:**
   Modify the watcher configuration or code (located at `/app/watcher.py` and its config `/app/watcher.conf`) so that it executes `/home/user/filter.py <filepath>` whenever a file is detected.
   * If the filter exits `0`, the watcher should push the file to Redis as normal.
   * If the filter exits `1`, the watcher MUST NOT push the file to Redis. Instead, it should append the filename to `/home/user/quarantine.log`.

**Constraints:**
- Use standard Python 3. You may use shell commands to adjust configurations, but the filter logic must be in `/home/user/filter.py`.
- Do not modify `builder.py` or the Nginx setup. Ensure the end-to-end flow (saving a safe file in `docs_src` -> served on port 8080) continues to work.