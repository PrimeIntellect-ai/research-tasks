You are a forensics analyst responding to a compromised Linux server. We have extracted some artifacts, including an intercepted audio recording of the attacker and a dump of recent HTTP traffic. The attacker seems to be using a custom C2 protocol embedded in HTTP requests, exploiting an XSS vulnerability, and occasionally leaking host credentials via HTTP GET query parameters.

Your objective is to create a Go-based intrusion detection classifier that will process raw HTTP request files and flag the malicious ones.

Here is what you need to do:
1. **Analyze the Audio Artifact:** We recovered an audio file at `/app/audio/intercept.wav`. You will need to transcribe it (e.g., using `whisper-cli`, `ffmpeg`, or similar tools which you can install) to understand the attacker's specific TTPs. The attacker explicitly mentions the custom HTTP header they use for C2 communication and the specific HTML tag/event handler combination they use for their XSS payloads.

2. **Develop the Classifier:** Write a Go program at `/home/user/scanner.go`. This program will be invoked by our automated verification suite exactly like this:
   `go run /home/user/scanner.go <path_to_http_request_file>`

   Your program must read the raw HTTP request from the given file path, inspect the headers and URI, and print exactly one word to `stdout`:
   - `CLEAN` if the request is benign.
   - `EVIL` if the request is malicious.

3. **Classification Rules:**
   A request is `EVIL` if it meets ANY of the following criteria:
   - It contains the custom C2 HTTP header mentioned in the audio intercept.
   - The body or URI contains the exact XSS injection pattern mentioned in the audio intercept.
   - It leaks credentials in the URI query string (specifically, any query parameter named `password`, `pwd`, or `secret_token` that has a non-empty value).
   - It contains SQL injection payloads in the URI (look for `UNION SELECT` or `' OR 1=1`).

   Otherwise, the request is `CLEAN`.

You must ensure your Go program handles malformed HTTP requests gracefully (treating them as EVIL if they violate basic HTTP structures, though the corpora mostly consist of well-formed requests). You are free to use any standard Go libraries (`net/http`, `bufio`, `regexp`, etc.). 

Do not rely on external services for the core logic of the Go script. Once your script is ready, you can test it, but the final evaluation will automatically run your script against a hidden adversarial corpus of evil and clean HTTP requests.