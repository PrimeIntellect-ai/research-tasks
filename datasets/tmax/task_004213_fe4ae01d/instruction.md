You are tasked with building a configuration tracking and application script for a legacy system. 

First, you need to recover the system's baseline configuration. A technician recorded the boot sequence, which flashes the baseline configuration archive in chunks. You will find this video at `/app/config_scroll.mp4`. 
1. Use `ffmpeg` to extract the frames from this video.
2. The video contains exactly 5 frames with distinct text (one every 2 seconds in a 10-second 1fps video). Each frame contains a base64-encoded string.
3. Extract the text from these frames (e.g., using `tesseract`). 
4. Concatenate the 5 base64 strings in chronological order, decode the combined base64 string, and uncompress the resulting `tar.gz` archive.
5. Inside, you will find `base.ini`. Place `base.ini` in `/home/user/base.ini`.

Next, write a Bash script at `/home/user/apply_config.sh` that takes a stream of configuration changes via standard input (stdin), applies them to the state found in `/home/user/base.ini`, and outputs the resulting INI file to standard output (stdout).

The input changelog format consists of lines with the following syntax:
`ADD <section> <key> <value>` - Adds a new key-value pair to a section. If the section doesn't exist, it is created.
`MOD <section> <key> <new_value>` - Modifies an existing key. If the key or section doesn't exist, ignore the command.
`DEL <section> <key>` - Deletes a key. If the section becomes empty, the section remains. If the key doesn't exist, ignore.

Your script must parse standard input line-by-line, update the configuration state, and print the final INI state.
The output MUST be perfectly formatted as a standard INI file, with sections sorted alphabetically, and keys within each section sorted alphabetically. 
Example output format:
```
[Network]
IP=192.168.1.1
Port=8080
[System]
Hostname=server01
```

Requirements:
- Only use standard Bash tools (awk, sed, grep, etc.). Do not use Python, Perl, or other interpreters for the script.
- Ensure your script safely handles temporary files (if any are used) by using atomic writes and trapping exits to clean up.
- Your script will be rigorously tested against hundreds of random changelog streams to ensure it precisely matches the expected output of a reference system.