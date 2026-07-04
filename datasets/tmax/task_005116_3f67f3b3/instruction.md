You are a deployment engineer tasked with rolling out a secure audio processing pipeline. You have inherited a system that is currently under attack by malicious actors submitting malformed audio files to crash the backend (via memory exhaustion). 

Your task consists of three main phases:

**Phase 1: Deployment Authorization (Audio Fixture)**
The lead engineer left the new backend migration port in a voicemail.
1. Transcribe the audio file located at `/app/deployment_voicemail.wav`. You may install and use any tools necessary (e.g., `ffmpeg`, `whisper-cpp`, or python libraries) to listen to or transcribe the file.
2. The voicemail will state the migration port number. Save this port number (as digits, e.g., `1234`) in a file called `/home/user/deploy_port.txt`.

**Phase 2: Port Forwarding and Storage Limits**
1. Set up a local SSH tunnel that forwards your local port `8080` to the migration port discovered in Phase 1 on `localhost`. Ensure this tunnel runs in the background.
2. The audio processing worker requires strict limits to prevent disk exhaustion. Create a bash wrapper script at `/home/user/worker_wrapper.sh` that first sets a maximum file size limit (disk quota) of 50 MB (using the standard shell built-in for resource limits), and then executes the command passed to it as arguments.

**Phase 3: The C++ Audio Validator (Adversarial Corpus)**
The malicious files causing the crashes are disguised as standard WAV files but contain malformed chunk headers (specifically, `data` chunks claiming to have a size greater than 100 MB).
1. Write a C++ program at `/home/user/validator.cpp` and compile it to `/home/user/validator`.
2. The program must accept exactly one command-line argument: the path to a WAV file.
   Usage: `./validator /path/to/file.wav`
3. The program must parse the RIFF/WAVE header and iterate through the chunks. 
4. If the file is not a valid RIFF/WAVE file, or if *any* chunk specifies a size greater than `100000000` bytes (100MB), the program must exit with a non-zero status code (e.g., `1`), effectively rejecting the file.
5. If the file has a valid structure and all chunks are under the size limit, the program must exit with status code `0` (accepting the file).
6. Test your compiled validator against the provided test corpora:
   - Valid audio files are located in `/app/corpus/clean/`
   - Malformed/malicious audio files are located in `/app/corpus/evil/`
   
Your solution will be evaluated automatically. Your validator must accept 100% of the clean corpus and reject 100% of the evil corpus.

Ensure your code is robust, compiles cleanly with standard `g++`, and accurately handles little-endian byte parsing for WAV headers.