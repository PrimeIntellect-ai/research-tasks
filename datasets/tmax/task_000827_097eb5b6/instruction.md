You have recently inherited an unfamiliar codebase for a network telemetry analysis system. The system processes captured network traffic to generate statistical models of packet flows. Recently, the pipeline has been experiencing intermittent failures and numerical instabilities (reporting `NaN` values for flow statistics), eventually leading to outright crashes. 

Your investigation has revealed that the pipeline relies on a heavily modified, vendored version of the `dpkt` library to parse packets. The previous developer left behind a raw memory dump of the application's heap at the exact moment of a crash, but no documentation.

Your objectives are:

1. **Memory Dump Analysis & Extraction:**
   Analyze the binary memory dump located at `/app/dumps/crash.bin`. The crash was caused by a specific "poisoned" packet payload that triggered the intermittent failure. Extract the unique byte sequence or string signature of this malformed payload from the dump. 

2. **Fix the Vendored Package:**
   The parsing library is located at `/app/vendored/dpkt-1.9.8`. The previous developer made an experimental change in the codebase that introduced a numerical instability when parsing specific packet headers, causing checksums or lengths to occasionally evaluate to `NaN` instead of integers, which poisons downstream mathematical models. Identify and fix this deliberate perturbation in the vendored `dpkt` source code so that the library correctly parses standard network packets without introducing `NaN`s. You must install your fixed version into the local Python environment.

3. **Develop a Malicious Payload Detector:**
   Using the fixed `dpkt` library and the signature extracted from the memory dump, write a Python detection script at `/home/user/detector.py`. 
   The script must accept a single command-line argument (the path to a `.pcap` file).
   - If the file contains the poisoned payload signature or triggers the numerical instability, the script must print `EVIL` and terminate with exit code `1`.
   - If the file is benign, the script must print `CLEAN` and terminate with exit code `0`.

To verify your detector, you must ensure it perfectly categorizes the packets in the provided test directories:
- Benign traffic is located in `/app/corpora/clean/`
- Malicious traffic (containing the crash-inducing payloads) is located in `/app/corpora/evil/`

Ensure your detector is highly efficient and relies strictly on standard Python libraries alongside the fixed `dpkt` package.