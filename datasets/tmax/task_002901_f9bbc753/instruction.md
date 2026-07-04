You are an AI assistant helping a technical writer organize a continuous stream of documentation.

We have a multi-service documentation system located in `/app/`.
The system consists of:
1. An incoming doc service that writes metadata files to `/app/incoming/`
2. An Nginx server that is supposed to serve organized documentation on port 8080.
3. A background watcher that triggers a processing script when new metadata arrives.

Your task has two parts:

Part 1: Service Configuration
The Nginx server is currently misconfigured. It is trying to serve files from `/var/www/html` on port 80. You must modify `/app/nginx.conf` so that it listens on port 8080 and serves the directory `/app/docs/`. Make sure Nginx has the right permissions and configurations to follow symlinks (using `disable_symlinks off;`). 
Update the background watcher configuration file `/app/watcher.conf` to point `PROCESS_SCRIPT` to `/home/user/parse_docs.sh`.

Part 2: Write the Parsing Script
You must write a bash script at `/home/user/parse_docs.sh` that reads a custom metadata stream from standard input (stdin) and performs file operations. 
The input consists of multiple records separated by a blank line. Each record has the following format:
```
PATH: /absolute/path/to/source.md
AUTHOR: Author Name
TAGS: tag1, tag2, tag3
```

For each record, your script must:
1. Parse the fields.
2. For each tag, create a directory `/app/docs/by-tag/<tag>/` if it does not exist.
3. Safely acquire a lock on `/app/docs/.lock` to prevent race conditions during file operations.
4. Create a symbolic link in `/app/docs/by-tag/<tag>/<filename>` pointing to the absolute path specified in `PATH` (where `<filename>` is the basename of the file).
5. Output exactly the following format to standard output (stdout) for each parsed record:
`[AUTHOR] processed [filename] with [N] tags`
where `[N]` is the number of tags.

Your script must handle arbitrary whitespace around the colons and commas. It must only use standard bash built-ins and coreutils (awk, sed, grep, etc.).

Ensure your script is executable. You can test your setup by writing a sample metadata file to `/app/incoming/` and ensuring the symlinks appear and Nginx serves them.