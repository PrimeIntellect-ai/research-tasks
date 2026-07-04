You are a forensics analyst recovering evidence from a compromised Linux host. The attacker bypassed the host's custom authentication service, which relies on a proprietary token parser. We have recovered a set of suspected authentication token files from the host.

Your task has two parts:

1. **Audit and Fix the Vendored Token Parser:**
   The source code for the custom token parsing library and its CLI tool is located at `/app/libtokenparse-1.0/`. 
   - Identify and fix the CWE (vulnerability) in `tokenparse.c` that allowed the attacker to crash the service or bypass authentication. 
   - The Makefile in that directory was also sabotaged by the attacker so it no longer builds correctly. Fix the Makefile.
   - Compile the CLI tool `verify_token` by running `make`.

2. **Build a Detector for Malicious Evidence:**
   We have two corpora of recovered tokens:
   - `/app/corpus/clean/`: Contains normal, safe authentication tokens.
   - `/app/corpus/evil/`: Contains malicious tokens crafted by the attacker to exploit the vulnerability you just fixed.

   Create an executable bash script at `/home/user/detect.sh`. This script must:
   - Take exactly one argument: the absolute path to a token file.
   - Use your fixed `/app/libtokenparse-1.0/verify_token` to analyze the file.
   - Exit with status code `0` if the token is completely safe/clean.
   - Exit with status code `1` if the token is malicious (i.e., it attempts to trigger the vulnerability).

Your solution will be tested against both the clean and evil corpora. It must correctly classify 100% of the files in both directories without crashing.