You are a backup administrator managing a server with several Go microservices. 

There is a directory located at `/home/user/projects` containing various source files, binaries, and logs. Some of the Go source files contain sensitive information and must not be included in the standard backup. Furthermore, we only want to back up files that have been modified recently.

Your task is to write a Go program at `/home/user/backup_manager.go` that performs the following steps when executed:
1. Scans the `/home/user/projects` directory recursively.
2. Identifies all `.go` files that have been modified within the last 48 hours (from the time the program is run).
3. Reads the contents of these recent `.go` files to check if they contain the exact string `// SENSITIVE`. 
4. If a file does NOT contain `// SENSITIVE`, add it to a new gzip-compressed tarball archive located at `/home/user/archive.tar.gz`. The paths inside the tarball should be relative to `/home/user/projects` (e.g., `app1/main.go`).
5. For every file successfully added to the archive, write its full absolute path to a text file at `/home/user/archived_files.txt`, with one path per line.

Do not use any external third-party Go modules; rely only on the Go standard library (`archive/tar`, `compress/gzip`, `path/filepath`, `os`, `strings`, `time`, etc.).

Once you have written and tested your Go program, please leave it at `/home/user/backup_manager.go` so it can be automatically evaluated.