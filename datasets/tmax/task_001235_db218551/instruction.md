You are a Database Reliability Engineer tasked with ensuring the integrity of our hierarchical backup chains. 

Recently, our backup metadata system suffered an injection attack, leaving us with a mix of valid and corrupted backup manifests. Our Lead DBA left a voice memo before going on leave detailing the strict rules for what constitutes a valid backup hierarchy.

We have a collection of manifest files. Each manifest file represents a backup dependency graph, where each line contains two space-separated node IDs representing a "child parent" dependency relationship (e.g., `backup2 backup1` means backup2 depends on backup1).

Your tasks:
1. Locate and process the DBA's voice memo located at `/app/dba_memo.wav` (you may use available command-line tools like `whisper` or `ffmpeg` if needed, or simply extract the hidden metadata if it's embedded). The memo contains the precise rules for a valid backup graph.
2. Write a Bash script at `/home/user/validate_manifest.sh` that validates a given manifest file.
3. The script must accept exactly one argument (the path to a manifest file).
4. The script must exit with code `0` if the manifest is fully valid according to the DBA's rules, and exit with code `1` (or any non-zero) if it violates ANY rule.
5. Your script must be robust enough to handle recursive/hierarchical path resolution in Bash without infinite looping if a cycle is present.

Your solution will be tested against a hidden adversarial corpus. It must perfectly accept all clean manifests and correctly reject all evil ones.