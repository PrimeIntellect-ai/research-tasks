You are tasked with stepping in for a build engineer who left a critical dependency resolution script unfinished.

We have an artifact database containing metadata about various shared libraries, their semantic versions, ABIs, and dependencies. The previous engineer left a voicemail at `/app/requirements.wav` detailing the strict business logic for how we must resolve and link these libraries.

Your goal is to write a Python CLI tool at `/home/user/resolve.py` that reads a JSON artifact database, resolves the dependencies for a given target library according to the rules in the voicemail, and outputs the final list of shared library filenames.

The JSON database is structured as a list of library objects:
```json
[
  {
    "name": "libCore",
    "version": "1.2.4",
    "abi": "sysv",
    "metadata": ["stable", "tested"],
    "deps": ["libMath", "libIO"]
  },
  ...
]
```

Your program must have the following exact CLI interface:
`python3 /home/user/resolve.py --db <path_to_json> --target <library_name>`

Output format:
Print the resolved library filenames (`<name>.so.<version>`) to `stdout`, one per line, in the order they are resolved. Do not print anything else to `stdout`.

Constraints & Details:
- You will need to transcribe or listen to `/app/requirements.wav` to understand the filtering (ABI, version constraints, metadata rules) and the traversal order (e.g., BFS vs DFS) required to select the correct libraries.
- Standard SemVer 2.0.0 rules apply for version comparison.
- You must handle complex resolution graphs.
- Use any necessary Python libraries (you may install tools via `pip` or `apt` to transcribe the audio if needed).
- The automated verification system will test your script against 100 randomly generated artifact databases to ensure it perfectly matches the expected behavior.