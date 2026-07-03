You are an incident responder investigating a recent breach. The attacker successfully bypassed the web application firewall (WAF) by using a custom obfuscation tool to encode their malicious payloads (SQL injection and XSS). 

During forensic analysis, you recovered the attacker's custom obfuscation tool, a stripped ELF binary located at `/app/obfuscator`. 

Your goal is to understand how this binary obfuscates payloads and write a custom detection script in Python to identify these obfuscated payloads in our web logs.

**Instructions:**
1. **Analyze the Binary:** Reverse engineer or interactively analyze the stripped binary at `/app/obfuscator` to determine the exact obfuscation algorithm it applies to input strings. You may use tools like `strings`, `objdump`, `gdb`, or simply treat it as an oracle by feeding it inputs.
2. **Develop a Detector:** Write a Python script at `/home/user/detector.py`. 
    * The script must accept a single command-line argument: the path to a text file containing one URL-decoded HTTP query parameter string per line.
    * The script must read the file and determine if each line contains an obfuscated malicious payload (XSS or SQLi) encoded by the `/app/obfuscator` tool.
    * For each line in the input file, your script must print exactly one word to standard output: `EVIL` if it contains the obfuscated payload, or `CLEAN` if it does not.
    * Do not print anything else (no debug logs, no blank lines).

**Testing Your Detector:**
You must ensure your script has a 0% false positive rate and a 0% false negative rate. The automated verification system will run your script against two hidden corpora:
* A clean corpus of benign HTTP parameters.
* An adversarial corpus of parameters containing sophisticated SQLi and XSS attacks obfuscated with the recovered tool.

Your script will be invoked by the verifier as follows:
`python3 /home/user/detector.py <path_to_corpus_file>`

Complete your analysis and ensure `/home/user/detector.py` accurately implements the inverse logic or pattern matching required to catch the attacker's obfuscated payloads.