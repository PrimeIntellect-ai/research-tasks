You are a security engineer tasked with rotating credentials and replacing a legacy validation system. 

First, we need to recover the old reference certificates. A previous administrator left a voicemail with the password for the legacy keystore. Transcribe the audio file located at `/app/admin_voicemail.wav` to get the password, and use it to extract the certificates from `/app/legacy_keystore.p12` into `/home/user/certs/`.

Next, we need to analyze the legacy certificate validation binary. The binary is located at `/opt/legacy/validator`, but it is currently locked down. You will need to audit the system for a privilege escalation misconfiguration (hint: check sudoers or SUID binaries related to backups) to gain read access to this ELF file. Copy it to `/home/user/legacy_validator`.

Finally, we have lost the source code for `/home/user/legacy_validator`. By performing binary and ELF analysis on it, figure out exactly how it validates our custom certificate chain format (it reads a file path passed as the first argument, checks specific byte offsets, and returns an exit code). 

Your objective is to write a replacement program that perfectly mimics the behavior of the legacy validator. You may write this in any language, but it must be executable at `/home/user/new_validator` (make sure it has execute permissions and a shebang if it's a script). 

An automated test will generate thousands of random input files and pass them to both the original `/home/user/legacy_validator` and your `/home/user/new_validator`. Your program must produce the exact same standard output, standard error, and exit codes as the original binary for all inputs.