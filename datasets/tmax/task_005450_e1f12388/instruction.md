You are acting as a capacity planner for our global engineering infrastructure. We are standardizing our resource allocation for our virtualization (QEMU) nodes, CI/CD pipelines, and general storage. 

Our Lead Infrastructure Architect left a voicemail detailing the new routing rules for filesystem paths, but they are currently on a retreat with no internet access. 

Your task is to:
1. Locate the architect's voicemail at `/app/voicemail.wav`. Use standard transcription tools available on the system (e.g., `whisper` or `whisper.cpp` via `/usr/local/bin/whisper-cli`, or similar audio processing tools) to extract the spoken rules.
2. Create a bash script at `/home/user/allocate.sh` that acts as the capacity allocator. 
3. The script must take exactly one argument: a filesystem path (which may be a symlink, relative, or absolute).
4. The script must output the exact capacity allocation string based on the rules detailed in the audio recording. 
5. The script must strictly use Bash built-ins, coreutils, and standard CLI tools. It must be efficient and executable.

Make sure your script handles edge cases, such as resolving symlinks to their ultimate targets before evaluating the path rules, as paths are often heavily symlinked in our environment. The automated verifier will pass thousands of randomly generated paths (both existing and hypothetical) to your script to ensure its output perfectly matches the reference implementation.

Please ensure `/home/user/allocate.sh` has executable permissions.