You are acting as an artifact manager for a software repository. We recently discovered that some of the binary artifact bundles submitted by third-party vendors contain malicious macro payloads. 

We have a legacy, stripped binary at `/app/bin_extractor` that our system uses to unpack these bundles. Unfortunately, the vendor who wrote it went out of business, so we cannot modify it to add security checks. 

Your task is to create a Python script at `/home/user/filter.py` that acts as a pre-validation filter for incoming artifact bundles. 

**Requirements:**
1. **The Classifier:** Write `/home/user/filter.py`. It must accept a single command-line argument (the path to an artifact bundle). It must exit with code `0` if the bundle is safe (clean), and exit with code `1` if the bundle is malicious (evil).
2. **Corpora:** We have provided a set of known-good bundles in `/home/user/corpus/clean/` and known-bad bundles in `/home/user/corpus/evil/`. Use these to reverse-engineer how the malicious payloads are embedded and to test your filter.
3. **Configuration:** Your script must read `/home/user/policy.ini`, which contains rules and patterns for forbidden macros. You will need to parse this file, extract the embedded macros from the artifact (either by reverse-engineering the format or leveraging the `/app/bin_extractor` binary), and check the macros against the policy.

The bundles are constructed using file splitting, chunking, and custom binary structures. You must figure out how the macro text is stored and obfuscated to properly detect the malicious patterns before our system processes them.

Make sure your script is reliable. Automated verification will run your script against a hidden test set of clean and evil bundles and expects a 100% classification success rate.