You are an incoming security engineer tasked with updating our credential processing pipeline. We are rotating credentials and fixing a critical vulnerability in our microservices where JWTs with `algorithm: none` are being accepted. 

Your manager has left you a voicemail with instructions on how to access the new specifications.
The voicemail is located at `/app/voicemail.wav`.
A small dictionary of candidate base passwords is at `/app/wordlist.txt`.
The encrypted specifications and keys are in `/app/bundle.zip`.

Your objective is to:
1. Extract the instructions from the voicemail.
2. Use the clue in the voicemail to crack the password for `/app/bundle.zip`.
3. Read the specification inside the decrypted bundle.
4. Implement the required tool exactly as specified.

You must create an executable script at `/home/user/jwt_processor` (in the language of your choice) that exactly implements the logic described in the extracted specification. We will automatically test your script by feeding it thousands of random JWTs via standard input and comparing its standard output and exit codes against a reference implementation.

Requirements:
- Your script must be executable (`chmod +x /home/user/jwt_processor`).
- It must read a single JWT from `stdin`.
- It must output strictly to `stdout`.
- It must be bit-exact in its output and exit codes with the expected behavior defined in the specification.

You have full freedom to install any packages (e.g., `ffmpeg`, `whisper`, `fcrackzip`, or language runtimes) needed to transcribe the audio, crack the archive, and build your tool.