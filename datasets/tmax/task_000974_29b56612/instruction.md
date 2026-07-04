You are helping to organize and secure a project repository after a recent security incident. The security team has left a voice memo detailing the exact signatures of the compromised files. You can find this audio memo at `/app/security_memo.wav`.

Your task is to write a bash script at `/home/user/filter.sh` that takes a single directory path as its argument. 
When executed, your script must:
1. Create a `.quarantine` subdirectory inside the target directory if it does not already exist.
2. Scan all regular files in the target directory (non-recursively).
3. Determine if each file is "compromised" based on the rules specified in the audio memo.
4. Move any compromised files into the `.quarantine` subdirectory.
5. Leave all clean project files untouched in their original location.

Make sure your script is robust, uses standard bash tools, and is marked as executable. Do not process files inside subdirectories of the target directory (except for moving compromised files into `.quarantine`).