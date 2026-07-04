You are a security researcher analyzing an adversarial attack against a numerical tracking system. A malicious actor has successfully crashed our automated targeting pipeline by injecting corrupted telemetry via a hijacked video feed. 

We have captured a snippet of the attack in `/app/exfiltration_capture.mp4`. 

Additionally, we have isolated several JSON payloads that simulate the attacker's inputs. The attack exploits a mathematical vulnerability in our tracker (causing extreme precision loss and convergence failure in our numerical solver) by feeding it carefully crafted denormalized floats and corrupted arrays.

Your task has two main phases:

**Phase 1: Telemetry Extraction & Debugging**
1. Extract the raw telemetry frames from `/app/exfiltration_capture.mp4`. 
2. A buggy extraction script is provided at `/app/extract_telemetry.py`. It is supposed to parse frame metadata into a JSON list of floating-point values, but it suffers from precision loss and crashes on corrupted inputs (e.g., frames with artifacts). 
3. Debug and fix `/app/extract_telemetry.py` so it accurately extracts the full telemetry sequence to `/app/extracted_payload.json` without failing.

**Phase 2: Adversarial Detector Construction**
To prevent future attacks, we need a robust input sanitizer that mathematically verifies if a payload is safe before passing it to the tracker.
1. Inspect the provided corpora located in `/app/corpus/clean/` (safe telemetry sequences) and `/app/corpus/evil/` (adversarial sequences that cause convergence failures or precision crashes).
2. Create a Python script at `/app/detector.py`.
3. `detector.py` must take a single command-line argument: the path to a JSON file containing a telemetry array.
4. The script must analyze the numerical properties of the array and determine if it is an attack payload.
   - If the payload is SAFE (clean), it must exit with code `0`.
   - If the payload is MALICIOUS (evil), it must exit with code `1`.

Your `detector.py` must perfectly classify the payloads in `/app/corpus/clean/` and `/app/corpus/evil/`.