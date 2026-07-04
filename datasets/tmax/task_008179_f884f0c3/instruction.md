You are helping migrate an old build system component from Python 2 to Python 3. 

We have a legacy script located at `/home/user/dep_resolver.py` that processes a simulated shared library dependency graph (from `/home/user/deps.json`). It uses a custom graph data structure to resolve dependencies via depth-first search, and computes an error-detecting checksum for the entire dependency tree.

Because this script was written for Python 2, it currently fails to run under Python 3. It suffers from several common Python 2/3 migration issues, including syntax errors, outdated exception classes, and string/bytes encoding mismatches when computing hashes.

Your task is to:
1. Fix the script `/home/user/dep_resolver.py` so it executes successfully using `python3`.
2. Ensure the script correctly calculates the checksum for the target node `"app"`. Note that in Python 3, `hashlib` requires byte-like objects, not regular strings. You should encode all strings to `utf-8` before passing them to the hash update method.
3. Run the script. The script is already programmed to write the final computed checksum for `"app"` to `/home/user/checksum.txt`.

Ensure the final checksum is correctly written to `/home/user/checksum.txt`. Do not change the logic of the graph traversal or the checksum algorithm, only apply the necessary language-level migration fixes.