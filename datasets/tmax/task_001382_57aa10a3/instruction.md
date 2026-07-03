You are an integration developer responsible for testing and deploying a new internal API that interprets a custom concurrency Domain Specific Language (DSL), known as "GoLite". 

Your task consists of four main stages:

**Stage 1: Environment Resolution**
The project currently has a broken Python dependency setup in `/home/user/project/`. When you try to install the dependencies (`pip install -r requirements.txt`), it fails due to severe version conflicts between `fastapi`, `pydantic`, `starlette`, and a custom internal testing library. 
Analyze the dependency tree, resolve the conflicts, and successfully install the packages into a virtual environment at `/home/user/project/venv`. You must retain FastAPI and Pydantic, but you may need to pin specific compatible versions.

**Stage 2: Audio Specification Extraction**
The lead architect left the final DSL API specifications in an audio memo located at `/app/instruction.wav`. Use any available tool (e.g., `ffmpeg`, `whisper`, or a python audio transcription library of your choice that you can install) to transcribe this file. The audio contains critical instructions regarding specific malicious patterns in the DSL that must be blocked. Save the exact transcript to `/home/user/project/transcript.txt`.

**Stage 3: GoLite DSL Interpreter API**
Implement a REST API in Python (using the fixed FastAPI setup) at `/home/user/project/server.py` that listens on port 8000. 
Create an endpoint `POST /execute` that accepts a plain-text GoLite script.
GoLite scripts simulate Go concurrency patterns. Your interpreter must support:
- `SPAWN <func>`: Executes a block asynchronously.
- `CHAN <name>`: Creates a message channel.
- `SEND <chan> <val>`: Sends a value to a channel.
- `RECV <chan>`: Receives a value from a channel.
Use Python's `asyncio` to emulate this behavior. The endpoint should return a JSON array of all values successfully received from channels during the execution of the script, timing out after 2 seconds.

**Stage 4: Adversarial Sanitizer**
The API is vulnerable to malicious GoLite scripts (e.g., fork bombs, infinite loops, illegal system calls). 
Based on the rules extracted from the audio memo, write a script at `/home/user/project/sanitizer.py` that can classify a GoLite script.
It must be executable via the command line:
`python3 /home/user/project/sanitizer.py <path_to_script>`
- It should exit with code `0` if the script is CLEAN.
- It should exit with code `1` if the script is EVIL.

We have provided a training/validation corpus:
- Clean scripts: `/app/corpus/clean/`
- Evil scripts: `/app/corpus/evil/`

Your sanitizer must correctly reject all scripts in the evil directory while preserving/allowing all scripts in the clean directory.

Ensure your API integrates the sanitizer to block evil requests with an HTTP 400 status code.