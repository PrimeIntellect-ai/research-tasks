I am a developer debugging an intermittently failing build in our system. The build process relies on a Bash script to compute mathematical checksums, but the original script was recently accidentally deleted and replaced by a corrupted backup (`/home/user/checksum.sh`) that suffers from encoding issues and intermittent race conditions.

Fortunately, the senior engineer who designed the original system left a voicemail detailing the exact mathematical formula required for the checksum. This audio file is located at `/app/voicemail.wav`.

Please help me fix the build by doing the following:
1. Analyze the audio file at `/app/voicemail.wav` to recover the correct mathematical formula for the checksum. 
2. Delete the corrupted `/home/user/checksum.sh`.
3. Create a new, robust Bash script at `/home/user/checksum.sh` that implements the formula described in the voicemail.
4. The script must take exactly one argument (an integer), perform the mathematical operations described, and output only the final integer result to standard output. 
5. Make sure the script is executable (`chmod +x`). 

You may use any transcription tools available in the environment (like `whisper` or `ffmpeg`) to decode the audio. The automated build system will rigorously test your script against thousands of random integers to ensure it is bit-exact equivalent to the original lost implementation.