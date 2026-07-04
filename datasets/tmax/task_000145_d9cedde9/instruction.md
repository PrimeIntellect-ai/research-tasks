You are a performance engineer tasked with profiling application traffic. A colleague wrote a Python script, `/home/user/pcap_processor.py`, to parse a directory of network packet captures (`/home/user/pcaps/`) and calculate the total volume of traffic in bytes. 

However, the script has a few critical bugs:
1. It intermittently outputs different results on subsequent runs (intermittent failure).
2. It seems to completely ignore some capture files.

Your task:
1. Debug `/home/user/pcap_processor.py` to identify and fix the underlying issues. The script is supposed to sum the lengths of all packets across all `.pcap` files in `/home/user/pcaps/`.
2. Ensure that it correctly and reliably processes all files and accurately calculates the total packet length.
3. Run the fixed script. It must write the correct final integer sum to `/home/user/result.txt`.

Do not modify the test directory `/home/user/pcaps/` or rename the files inside it. Fix the script so it handles the existing files correctly. You may install standard analysis tools like `tcpdump` or `scapy` if they are not present.