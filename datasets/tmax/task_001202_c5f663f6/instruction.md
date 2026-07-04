You are an artifact manager tasked with curating a large binary repository. We need a tool to scan directories, interpret artifact manifest files, normalize their character encodings, and produce a consolidated summary. 

Before you write the tool, you must fix a dependency. We use a local, vendored version of the `toml` package located at `/app/toml-0.10.2`. However, a recent rogue commit broke it. 
1. Identify the deliberate syntax error/typo that was introduced into the `toml` package's source code and fix it.
2. Install the fixed package into your Python environment.

Once the dependency is fixed, write a Python 3 script at `/home/user/curate.py` that does the following:
1. Accepts exactly one command-line argument: an absolute path to a target directory.
2. Recursively searches the target directory for all files with the `.manifest` extension.
3. Reads each manifest file. Manifests are TOML configuration files, but they may be encoded in `UTF-8`, `UTF-16LE`, or `CP1252`. Your script must cleanly read them (try `utf-8`, fallback to `utf-16le`, then `cp1252`).
4. Parses the TOML content. Each manifest contains a `[metadata]` section with `artifact_name`, `version`, `architecture`, and `status`.
5. Filters the artifacts, keeping ONLY those where `status` is exactly the string `"released"`.
6. Prints a consolidated JSON array to standard output (`stdout`). The JSON must be an array of objects, with each object having the keys `"name"`, `"version"`, and `"arch"` (mapped from the TOML keys).
7. The JSON array must be sorted alphabetically by the artifact's `"name"` in ascending order. Do not pretty-print (no extra newlines/indentation in the JSON array).

Your script must be strictly deterministic and bit-exact equivalent to our reference implementation when provided the same directory.