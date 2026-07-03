You are a Build Engineer responsible for managing compiled artifacts and their versioning systems. Our legacy CI system crashed, but we managed to recover a video screen-recording of the test matrix run, which contains embedded metadata about blacklisted artifact versions. We need you to restore the artifact resolution tool using only Bash.

Part 1: Video Analysis
A video artifact is located at `/app/build_metrics.mp4`. The video contains a subtitle stream (stream 0:1) that displays the semantic versions of artifacts that failed integration testing and are permanently blacklisted.
Extract the text of these subtitles and save them into a file at `/home/user/blacklist.txt` (one semantic version per line, clean of any subtitle formatting).

Part 2: Semantic Version Resolution
Write a Bash script at `/home/user/resolve_artifacts.sh` that determines the highest compatible artifact version for a given request. 
The script must take exactly two arguments:
1. `requested_version_range`: A semver range (e.g., `^1.2.0`, `~2.3.4`, or an exact version `1.2.3`).
2. `available_versions_file`: The path to a text file containing a list of available semantic versions (one per line).

The script must:
- Read the available versions from the specified file.
- Ignore any versions that appear in `/home/user/blacklist.txt`.
- Compare the remaining versions using standard semantic versioning rules (Major.Minor.Patch).
- Resolve the `requested_version_range` correctly:
  - `^X.Y.Z` allows changes that do not modify the left-most non-zero element.
  - `~X.Y.Z` allows patch-level changes if a minor version is specified.
- Output ONLY the single highest compatible version string to standard output. If no version matches, output `NONE`.

Ensure your script handles complex version parsing natively in Bash, using arrays and custom parsing functions to build the data structure for semantic version comparison.