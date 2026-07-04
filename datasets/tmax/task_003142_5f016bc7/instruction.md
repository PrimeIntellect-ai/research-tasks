You are an artifact manager curating binary repositories for a secure production environment. You need to build a system that monitors a spool directory for incoming artifact manifests, parses them, handles character encoding anomalies, and sanitizes the metadata to prevent malicious injections or path traversals.

Your task consists of three main stages:

**Stage 1: Fix and Build the File Watcher**
We vendor a specific version of our file-watching dependency, `inotify-tools`, located at `/app/vendor/inotify-tools-3.22.6`.
However, the source contains a deliberate perturbation introduced during a botched backport. 
1. Identify and fix the C source compilation error in the `inotify-tools` source.
2. Compile and install it so that the binary `inotifywait` is available at `/home/user/local/bin/inotifywait`.

**Stage 2: Artifact Manifest Sanitizer**
You must write a Bash script at `/home/user/sanitize_manifest.sh`. This script will be used to validate incoming `.manifest` files. 
Usage: `/home/user/sanitize_manifest.sh <path_to_manifest>`

Manifest files contain multi-line records formatted as:
```
[Artifact: <ArtifactName>]
Path: <RelativeFilePath>
Hash: <SHA256>
Description: <Multi-line text ending with a blank line>

```
*Encoding Issues:* Incoming manifests originate from different legacy systems. Some are encoded in `UTF-16LE` (with or without BOM) and others in `Windows-1252`. Your script must detect the encoding and convert the content to `UTF-8` before parsing.
*Validation Rules:*
- **Clean/Valid:** The script must output the standard UTF-8 converted text to `stdout` and exit with code `0`. Valid names contain alphanumeric characters, hyphens, and underscores. Paths must be strictly relative (e.g., `bin/app`, `lib/libfoo.so`). Hashes must be exactly 64 lowercase hex characters.
- **Evil/Invalid:** The script must exit with a non-zero code and print nothing to stdout if ANY of the following are detected:
  - Path traversal attempts (e.g., containing `../` or starting with `/`).
  - Shell injection characters in the `<ArtifactName>` (e.g., `$`, `` ` ``, `<`, `>`, `|`, `;`).
  - Invalid hash lengths or non-hex characters in the `<SHA256>` field.
  - Malformed multi-line structure (missing required headers).

**Stage 3: Testing**
Ensure your script `/home/user/sanitize_manifest.sh` correctly classifies malicious vs safe manifests. We will test it against a hidden adversarial corpus of manifests upon submission.