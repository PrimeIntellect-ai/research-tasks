You are an infrastructure engineer automating the provisioning of QEMU virtual machines. We need a lightweight, custom provisioning daemon written in C that handles VNC access control lists (ACLs) based on a voice-transmitted authorization passcode.

We received an automated voicemail containing the new provisioning passcode. The audio file is located at `/app/vm_auth.wav`.

Your task is to:
1. Determine the exact passcode spoken in the audio file `/app/vm_auth.wav` (all lowercase, no punctuation, words separated by a single space).
2. Write a C program at `/home/user/prov_daemon.c` and compile it to `/home/user/prov_daemon`.
3. The daemon must run as a TCP server listening on `127.0.0.1:8111`.
4. When a client connects and sends the exact passcode (followed by a newline `\n`), the daemon must:
   a. Reply to the client with the string `VNC_ACL_UPDATED\n`.
   b. Create or overwrite a system configuration file at `/home/user/qemu_vnc.acl`.
   c. Write the exact text `VNC_ACCESS=GRANTED\n` to this file.
   d. Set the file permissions of `/home/user/qemu_vnc.acl` strictly to `0400` (read-only for owner, no access for group/others).
   e. Close the connection.
   (If an incorrect passcode is sent, the daemon can simply close the connection without modifying the file).
5. Start your daemon in the background so it is actively listening on port 8111. 

You may use any installed tools (e.g., Python, whisper, ffmpeg) to transcribe the audio file. Ensure the daemon is running before you consider the task complete.