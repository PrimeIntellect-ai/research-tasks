You are an incident responder investigating a recent data breach. We believe an attacker abused a legitimate administrative utility to exfiltrate credentials via process command-line arguments, which were temporarily visible in `/proc`.

The only direct evidence of the breach is a screen recording from a compromised jump host, available at `/app/incident.mp4`. 

Your objectives are:
1. **Analyze the Video**: Extract frames from `/app/incident.mp4` (using `ffmpeg`) to reconstruct the attacker's terminal session. Identify the specific tool used and the exact command-line argument pattern that constitutes the credential exfiltration (e.g., the specific flags and the nature of the target destination).
2. **Build a Detector**: Write a C program at `/home/user/detector.c` that parses a given command line and detects this exfiltration technique.
   - The program must compile to `/home/user/detector` without errors using `gcc /home/user/detector.c -o /home/user/detector`.
   - The program will be invoked with a single argument: the path to a text file containing a command line string. Example: `/home/user/detector /tmp/cmd.txt`
   - **Exit Code 1 (Reject)**: If the command line string matches the malicious exfiltration pattern observed in the video (specifically, using the tool to send credentials over an unauthorized network protocol scheme to an arbitrary IP).
   - **Exit Code 0 (Accept)**: If the command line represents normal administrative usage (e.g., legitimate flags, local file paths, or authorized internal destinations).

Assume the command line arguments in the text files are space-separated. Your C program must implement secure coding practices for input validation.

Do not write your detector to only hardcode the exact IP/password seen in the video; it must detect the general pattern of using that specific network protocol scheme for the target flag.