You are an infrastructure engineer automating the provisioning of edge servers. You have two critical tasks to complete regarding server verification and configuration filtering.

Part 1: Configuration Sanitization
Edge servers send provisioning configurations in JSON format. Some of these configurations have been compromised and contain malicious network or environment setups.
You must write a Python script at `/home/user/sanitize.py` that takes a JSON file path as its first argument.
- The JSON contains a dictionary.
- If the dictionary contains a key `"post_install_script"`, your script must analyze its string value.
- Reject the configuration if the script contains any of these forbidden substrings: `wget`, `curl`, `nc`, `/dev/tcp`, or `mkfifo`.
- To reject, your script must exit with status code `1`.
- If the configuration is safe (does not contain those strings), your script must print the raw JSON contents to standard output and exit with status code `0`.

Your script will be tested against a hidden suite of clean and malicious configuration files. It must correctly accept 100% of the clean configurations and reject 100% of the malicious ones.

Part 2: Boot Sequence Video Analysis
During provisioning, a camera records the diagnostic LED of the edge server. The recording is available at `/app/boot_sequence.mp4`.
You need to determine how many times the LED flashes red.
- Extract the frames of the video (e.g., using `ffmpeg`).
- Analyze the frames to count how many frames have a center pixel (width/2, height/2) that is predominantly red (Red > 200, Green < 50, Blue < 50).
- Write the total count as a single integer to `/home/user/led_flashes.txt`.

Ensure your python script `/home/user/sanitize.py` is executable and correctly implements the filtering logic.