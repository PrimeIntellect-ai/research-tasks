I am migrating a legacy project from Python 2 to Python 3. Before I can proceed with the automated migration tools, I need a fast Bash-based linter to identify files that contain specific legacy patterns that our automated tools can't handle properly.

My coworker left me an audio message at `/app/legacy_note.wav` detailing the exact Python 2 patterns we need to ban. 

Your task is to:
1. Transcribe or listen to `/app/legacy_note.wav` to find out what specific legacy patterns must be rejected.
2. Write a Bash script at `/home/user/check_py3_ready.sh` that takes a single Python file path as an argument (`/home/user/check_py3_ready.sh <path_to_file.py>`).
3. The script must parse the provided Python file and:
   - Exit with status `0` (success) if the file does NOT contain the forbidden legacy patterns (i.e., it is "clean").
   - Exit with status `1` (failure) if the file DOES contain ANY of the forbidden legacy patterns (i.e., it is "evil").

The script should be robust enough to handle basic variations in spacing (e.g., multiple spaces after `import`). You can use standard Unix utilities (grep, awk, sed) in your Bash script. Make sure the script is executable.

We will test your script against a hidden adversarial corpus consisting of a `clean` directory and an `evil` directory. Your script must correctly classify 100% of both corpora.