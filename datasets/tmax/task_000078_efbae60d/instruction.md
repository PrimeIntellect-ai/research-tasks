You are a Database Reliability Engineer (DBRE) managing a hybrid-database backup system. Our backup system uses PostgreSQL to store the hierarchical directory structure of the backed-up files and MongoDB to store the actual file contents broken down into chunks.

Your task is to write a cross-database restoration CLI tool.

### Environment Setup
The system relies on two services:
1. **PostgreSQL** (running on `localhost:5432`, user: `postgres`, password: `postgres`, db: `backups`)
2. **MongoDB** (running on `localhost:27017`, db: `backups`)

First, start the services and populate them with the initial dataset by running:
`/app/start_services.sh`

### Schema Information
You will need to analyze the schemas yourself, but here is a starting point:
- **PostgreSQL**: Contains tables `jobs`, `nodes`, and `files`. The `nodes` table represents a hierarchical directory structure (files and folders). You will need to use a recursive CTE to traverse from a root node down to all its children to reconstruct full file paths.
- **MongoDB**: Contains a collection `chunks`. Each document represents a chunk of a file's content, mapped by a `file_id`. 

### Your Goal
Write an executable tool located at `/home/user/restore_tool`. You may write it in any language available on the system (e.g., Python, Node.js, bash+psql+mongosh, etc.), but it must have executable permissions (`chmod +x`).

The tool must accept a single command-line argument: `--job-id <integer>`.

When executed, it should:
1. Connect to PostgreSQL and locate the root node for the given `job-id`.
2. Recursively traverse the hierarchy to find all files associated with this backup job, reconstructing their absolute logical paths (e.g., `/root/etc/config.txt`).
3. Connect to MongoDB to fetch the content chunks for each file.
4. Reassemble the file content by concatenating the chunks in the correct order (using a NoSQL aggregation pipeline or query sorting).
5. Output to `stdout` a strict JSON array containing an object for each file, with the following format:
```json
[
  {
    "path": "/var/log/syslog",
    "content": "Line 1\nLine 2..."
  },
  ...
]
```
The JSON array must be **sorted alphabetically by the `path` key**. 
Ensure the output is entirely bit-exact JSON, with no extraneous logging or warning messages on `stdout` (you may print logs to `stderr`).

Automated verifiers will extensively fuzz your `/home/user/restore_tool` against a hidden reference implementation with multiple job IDs to ensure equivalence.