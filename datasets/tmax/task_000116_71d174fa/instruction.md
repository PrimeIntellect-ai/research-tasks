You are tasked with helping a configuration manager track recent changes across several legacy configuration files.

We have a directory at `/home/user/configs` containing various `.conf` files. These files are legacy configuration files saved in the `ISO-8859-1` (or Windows-1252) character encoding. 

Your objective is to:
1. Write a Go program at `/home/user/tracker.go` that accepts a list of file paths as command-line arguments.
2. For each file, the Go program must:
   - Read the file and convert its contents from `ISO-8859-1` to `UTF-8`.
   - Interpret the configuration file (which follows a basic `key=value` format, ignoring `[section]` headers).
   - Extract the values for the keys `name` and `server_url`.
   - Print a single line to standard output in the format: `[name] -> [server_url]` (e.g., `Système -> https://api.example.com`).
3. Use shell commands (like `find` and `xargs`) to search for `.conf` files in `/home/user/configs` that meet **both** of the following metadata criteria:
   - Modified within the last 5 days (`-mtime -5` or equivalent).
   - File size is strictly less than 10 kilobytes.
4. Pass the files found in step 3 as arguments to your Go program, and redirect the standard output of the Go program to `/home/user/active_servers.txt`.

Ensure your Go code correctly handles the character encoding conversion so that accented characters (like `é` or `è`) are properly represented as UTF-8 in `/home/user/active_servers.txt`. You may use standard Go libraries or install third-party packages (like `golang.org/x/text/encoding/charmap`) if necessary.