I need your help debugging an intermittent failure in a custom C-based network packet processing daemon, `packetd`. The daemon monitors industrial control traffic. Recently, after a series of updates, it started crashing sporadically with a segmentation fault. 

I've captured a screen recording of the console when the crashes occur, located at `/app/crash_demo.mp4`. I also have a packet capture from the network during those crashes: `/app/traffic.pcap`. 

The repository for the daemon is located at `/home/user/packetd_repo`. It has about 200 commits. The `master` branch is currently crashing on certain edge-case data, while the `v1.0` tag is known to be stable.

Here is what you need to do:
1. **Analyze the Video & PCAP**: Watch the video to identify the specific timestamps or log sequences immediately preceding the crash. Use this to isolate the exact packet payload from `/app/traffic.pcap` that triggers the crash.
2. **Git Bisection**: Find the exact commit hash that introduced this regression between `v1.0` and `master`.
3. **Intermittent Failure Reproduction**: Write a simple C program or script that extracts the malicious payload and feeds it to the `packetd` binary to reliably reproduce the crash.
4. **Develop a Sanitizer**: The temporary workaround is to filter out these malicious packets before they reach the daemon. Write a standalone C program `/home/user/sanitizer.c` that takes raw packet payloads via standard input and outputs `1` (safe) or `0` (malicious/reject). 

The sanitizer will be tested against two corpora of raw payloads:
- A directory of benign payloads.
- A directory of adversarial/malicious payloads that trigger the bug.

Please compile your sanitizer to `/home/user/sanitizer`.

Finally, write the commit hash that introduced the bug to `/home/user/bad_commit.txt`.