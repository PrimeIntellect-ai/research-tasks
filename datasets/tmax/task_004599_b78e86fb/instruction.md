You are a forensics analyst investigating a compromised Linux host. The attacker left behind an audio recording of a VoIP transmission, modified a local web application, and established a hidden service. 

Your objective is to analyze the system, recover the attacker's backdoor logic, and create a detector to filter out malicious network traffic.

**Step 1: Service Auditing & File Integrity**
The attacker set up a hidden HTTP service on `localhost` on a port between 8000 and 8100. 
1. Scan the local ports to find this hidden service.
2. Download the file `manifest.sha256` from the root of this service.
3. Use this manifest to verify the integrity of the web application source files located in `/app/server/`. Identify the single file that has been modified by the attacker.

**Step 2: Audio Transcription & Analysis**
The attacker accidentally left an intercepted VoIP call snippet at `/app/voip_intercept.wav`.
1. Transcribe this audio file (you may use transcription tools like `whisper` or `ffmpeg` available in your environment). 
2. The audio contains the attacker dictating a 4-character alphanumeric "secret prefix".
3. Examine the modified source file from Step 1. You will see that the backdoor triggers only when an HTTP request contains a Cookie starting with this specific "secret prefix" AND a specific custom HTTP header used for command injection.

**Step 3: Build the Detector (Adversarial Corpus)**
The incident response team has captured raw HTTP requests and placed them in two directories:
* `/app/corpus/evil/` - Contains malicious requests that exploited the backdoor.
* `/app/corpus/clean/` - Contains benign requests (which may contain the header or the cookie prefix independently, but never the exact combination required to trigger the backdoor).

Write an executable script at `/home/user/detector` (you may use bash, python, etc., but it must be marked executable). 
* The script must take a single command-line argument: the absolute path to a file containing a raw HTTP request.
* It must exit with code `1` if the request is malicious (triggers the backdoor).
* It must exit with code `0` if the request is benign.

Your solution will be tested against the hidden corpora. You must successfully flag 100% of the files in the evil corpus and accept 100% of the files in the clean corpus.