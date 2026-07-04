You are tasked with building a configuration management utility in Rust that tracks differential changes between an old backup of server configurations and the current live configurations. 

In `/home/user/backup/v1/`, there is a backup of the previous configuration state.
In `/home/user/configs/`, there is the current live configuration state.

The configurations consist of flat JSON files and CSV files. Your goal is to write a Rust program that parses these structured formats, compares the new directory against the old directory, and generates a structured differential patch report.

**Step 1: Create the Rust Project**
Create a new Rust project named `config_tracker` in `/home/user/config_tracker`. You may add necessary dependencies like `serde`, `serde_json`, and `csv` to your `Cargo.toml`.

**Step 2: Implement the Diff Logic**
Write a CLI tool that accepts two arguments: the path to the old directory and the path to the new directory.
The tool must iterate through the files that exist in *both* directories and compare them based on their extension:

1. **For `.json` files**:
   - Assume the JSON files contain only flat, single-level objects with string keys and primitive values (strings, numbers, booleans).
   - Find keys that were added, removed, or modified (where the value changed).

2. **For `.csv` files**:
   - Assume the CSV files have a header row and the first column is a unique identifier (e.g., `id`).
   - Find rows that were added or removed (based strictly on the presence of the unique identifier in the first column). You do not need to track modified rows for CSVs.

**Step 3: Output Format**
The program must output a strictly formatted JSON object to standard output (`stdout`). The structure should match the following schema exactly:

```json
{
  "filename.ext": {
    "type": "json",
    "added": { "new_key": "value" },
    "removed": { "old_key": "value" },
    "modified": { "changed_key": { "old": 1, "new": 2 } }
  },
  "otherfile.csv": {
    "type": "csv",
    "added": [ {"id": "3", "col2": "val"} ],
    "removed": [ {"id": "2", "col2": "val"} ]
  }
}
```
*Note for CSV output: The added/removed arrays should contain objects representing the parsed rows, using the header names as keys. Values should be strings.*

**Step 4: Execution**
Build your Rust project and run it. Use bash stream redirection to pipe the output of your program to `/home/user/incremental_patch.json`:
`cargo run --release -- /home/user/backup/v1 /home/user/configs > /home/user/incremental_patch.json`

Ensure your output is valid JSON and perfectly matches the actual differences between the two directories.