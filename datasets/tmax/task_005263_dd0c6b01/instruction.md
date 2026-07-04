You are a compliance analyst reviewing a series of suspicious file upload incidents. Our system processes file uploads via a REST API, and we recently intercepted network logs that indicate a potential path traversal vulnerability being exploited, often paired with forged client certificates and unauthorized session tokens.

We have an audio log from the incident response team at `/app/incident_report.wav` which details the exact criteria used by the attackers.

Your task is to build a classifier that acts as an audit trail generator to separate legitimate requests from malicious ones.

1. Transcribe the audio file `/app/incident_report.wav` to discover the exact attack signatures you need to look for (which involve HTTP header inspection, payload decoding, and certificate validation).
2. The trusted Root CA for our internal services is located at `/app/trusted_ca.pem`.
3. Create an executable script at `/home/user/audit_classifier.sh` (you may write it in Bash, Python, or another standard language, but it must be executable via this path).
4. The script must take a single argument: the path to a text file containing a raw HTTP request.
5. The script must output EXACTLY the string `EVIL` (followed by a newline) if the request matches any of the malicious criteria described in the audio recording.
6. The script must output EXACTLY the string `CLEAN` (followed by a newline) if the request is benign.
7. To test your logic, two directories of sample requests are provided:
   - `/app/corpora/clean/`
   - `/app/corpora/evil/`

Your script must correctly classify 100% of the files in both corpora. You may need to install standard tools (like `openssl`, `base64`, `jq`, or python libraries) to inspect the certificate chains, decode the headers, and parse the cookies as instructed in the audio.