You are a security researcher analyzing a suspicious Python process that was caught beaconing to a command and control (C2) server. 

You have been provided with two files in the `/home/user/forensics/` directory:
1. `memdump.raw` - A raw memory dump of the compromised Python process.
2. `decode.py` - A reverse-engineered snippet of the malware's obfuscation routine used to decode its configuration.

Your task is to:
1. Extract the obfuscated C2 payload array from `memdump.raw`. The malware stores its encoded C2 URL as a comma-separated list of floating-point numbers enclosed by the markers `C2_OBF_START{` and `}`. Use standard shell tools to find and extract this array.
2. Feed the extracted float array to the `decode.py` script to recover the C2 domain.
3. You will notice that the decoded URL looks slightly garbled (e.g., wrong characters like `htto` instead of `http`). The malware author's decoding routine relies on floating-point arithmetic that suffers from precision loss, causing intermittent character corruption during Python's float-to-integer conversion.
4. Debug and fix the precision loss issue in `decode.py` so that it flawlessly decodes the original string.
5. Save the perfectly decoded, uncorrupted C2 URL to a file named `/home/user/c2_domain.txt`.

Ensure your final C2 URL does not contain any leading/trailing whitespace or the wrapper braces. Do not use external libraries outside the Python standard library.