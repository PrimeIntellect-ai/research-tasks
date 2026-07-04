**URGENT: 3 AM PAGE - `legacy-engine` exploit**

A critical security incident is ongoing. Our Python backend processes incoming binary payloads using a vendored legacy parsing library. The backend is periodically crashing, and we suspect malicious payloads are triggering arbitrary system calls (potentially remote code execution) in the underlying binary parser.

You need to perform the following steps to mitigate the incident:

**1. Restore the Vendored Package**
The proprietary parsing engine is located at `/app/vendored/legacy-engine`.
Recently, a junior developer accidentally broke the package. It now fails to run, complaining about a missing configuration/license secret. 
* Use your Git history forensics skills on the repository in `/app/vendored/legacy-engine` to recover the lost secret configuration.
* Figure out where the binary expects this secret to be placed (you may need to trace its system calls).
* Fix the environment so that `/app/vendored/legacy-engine/bin/engine` runs successfully against benign payloads.

**2. Analyze the Exploit**
We have captured a few sample payloads in `/app/samples/`. Some are safe, and some are exploits.
* Run the recovered `engine` binary against these samples.
* Use binary reverse engineering and/or system call tracing (`strace`) to observe the difference in execution between clean and malicious payloads.
* Deduce the encoding/format of the payloads and identify the precise signature or mechanism that triggers the malicious behavior.

**3. Build a Classifier**
Write a Python script at `/home/user/filter.py` that analyzes an incoming payload and detects if it is malicious, *without* relying on running the vulnerable binary.
* **Usage:** `python3 /home/user/filter.py <path_to_payload>`
* **Output:** The script must print exactly `CLEAN` to stdout and exit with code `0` if the payload is safe. It must print exactly `EVIL` and exit with code `1` if the payload contains the malicious exploit structure.

Your classifier will be tested against two hidden corpora. To pass, you must achieve 100% accuracy (rejecting all evil payloads and preserving all clean payloads).