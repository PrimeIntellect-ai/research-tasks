You are tasked with building a configuration state tracker in Go. 

As a configuration manager, our system receives periodic configuration backups as compressed archives. We use an incremental backup strategy: a base archive is created first, and subsequent archives only contain the files that have been modified or added since the previous backup.

Your goal is to write a Go program at `/home/user/tracker.go` that reads a sequence of these incremental backup archives, reconstructs the final logical state of the configurations, and outputs a specific summary report.

**Environment Details:**
- The backups are located in `/home/user/backups/`.
- The archives are named in alphabetical order representing their chronological sequence (e.g., `00_base.tar.gz`, `01_inc.tar.gz`, `02_inc.tar.gz`).
- You must process these archives directly using Go's compressed stream processing capabilities (e.g., `archive/tar` and `compress/gzip`). **Do not extract the archives to disk.**

**Contents of the Archives:**
The archives contain configuration files nested within various directories. The formats include JSON, XML, and CSV. You need to parse the following files to extract specific data:
1. `config/app.json`: Contains application settings. Extract the `version` (string) and `debug` (boolean) fields.
2. `config/database.xml`: Contains database settings. It has a root `<database>` element with `<host>` and `<port>` (integer) child elements. Extract both.
3. `config/network/routes.csv`: A CSV file with headers (e.g., `path,target`). Count the total number of route entries (excluding the header row).

*Note: Because these are incremental backups, a file might appear in multiple archives. The version of the file in the latest archive logically overwrites any previous versions.*

**Output Requirement:**
Once your Go program has processed all archives and reconstructed the final state, it must write a JSON file to `/home/user/final_state.json` with the following exact structure and keys:

```json
{
  "app_version": "<final version string>",
  "app_debug": <final debug boolean>,
  "db_host": "<final host string>",
  "db_port": <final port integer>,
  "route_count": <final number of routes integer>
}
```

**Task Steps:**
1. Write the Go script `/home/user/tracker.go` to implement the logic described above.
2. Build and run your script.
3. Ensure the output is correctly formatted and saved to `/home/user/final_state.json`.