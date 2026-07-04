You are managing an artifact repository where a chaotic build process dumps metadata into logs. Due to an aggressive, racing log-rotation script, multi-line artifact records are frequently split across log files. 

Your task is to write a Python script at `/home/user/parse_artifacts.py` that reconstructs these split multi-line records, parses out domain-specific data, and converts the findings into a structured JSON file.

The logs are located in `/home/user/logs/` and are named `build.log.2`, `build.log.1`, and `build.log`. The standard log rotation scheme applies: `build.log.2` is the oldest, `build.log.1` is newer, and `build.log` is the newest active log.

Each log record has the following structure (though it may be cut anywhere across file boundaries):
```
[RECORD_START] ID: <artifact_id>
TYPE: <GCODE or ELF>
DATA:
<... multiple lines of data ...>
[RECORD_END]
```

Requirements for `/home/user/parse_artifacts.py`:
1. Read the log files in chronological order (oldest first) to seamlessly stitch together records that were split during log rotation.
2. For records where `TYPE: GCODE`, parse the `DATA:` block to find the maximum `Z` coordinate (e.g., `Z10.5`, `Z-1.2`) among all `G0` or `G1` commands. 
3. For records where `TYPE: ELF`, parse the `DATA:` block to extract the entry point address (which will be on a line starting with `Entry point address: `).
4. Output a JSON file to `/home/user/curated_artifacts.json` mapping each artifact ID to its parsed metadata. 

The output JSON must strictly match this format:
```json
{
  "101": {
    "type": "GCODE",
    "max_z": 15.2
  },
  "102": {
    "type": "ELF",
    "entry_point": "0x401050"
  }
}
```

Run your Python script to generate the final `curated_artifacts.json` file.