You are tasked with diagnosing and fixing a failing systemd user service on this machine.

A systemd user service named `obfuscate-backup.service` was set up to periodically back up obfuscated file names, but it is currently failing to start. By inspecting the service logs, you will discover that it is failing because a critical C executable, `/home/user/backup/name_obfuscator`, is missing. The source code was accidentally deleted by a previous administrator.

You must recreate this C program. The program takes exactly one argument (a file path) and prints an obfuscated version of the path to standard output (without a trailing newline).

The obfuscation algorithm is as follows:
1. Extract the basename of the provided file path (everything after the last `/`). If there is no `/`, use the entire string.
2. Reverse the characters of the basename.
3. Prepend a specific secret prefix, followed by an underscore `_`, to the reversed basename. 

For example, if the prefix is `TEST`, running `./name_obfuscator /var/log/syslog` should output exactly `TEST_golsys`. If no arguments are provided, the program should return an exit code of 1. Otherwise, it should return 0.

The secret prefix is an uppercase word. It is not stored anywhere in plain text on the system, but it is visually documented in an old architectural diagram saved as an image at `/app/diagram.png`. You will need to extract the text from this image to find the prefix (it is the only text in the image). `tesseract` is installed on the system to assist with this.

Once you have determined the prefix, write the C code, compile it using `gcc`, and place the resulting executable exactly at `/home/user/backup/name_obfuscator`. Ensure the systemd user service can run successfully after your fix.