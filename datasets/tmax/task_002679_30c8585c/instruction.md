You are acting as an incident responder investigating a recent web server compromise. We have captured some artifacts left by the attacker, but we need your help to fully analyze and neutralize the threat.

Here is what we have:
1. An intercepted audio transmission left by the attacker, located at `/app/intercepted_comm.wav`. Our intelligence suggests this contains the passphrase required to unlock the main evidence archive. You will need to transcribe this audio (you may install and use tools like `whisper.cpp` or `ffmpeg` to process it). The audio contains spoken words in the NATO phonetic alphabet which spell out the password.
2. An encrypted zip archive at `/app/evidence.zip`. Once you obtain the password from the audio file, extract this archive into `/home/user/evidence/`. 
3. Inside the archive, you will find an obfuscated Linux binary named `payload_encoder`. The attacker used this binary to encode their web shell payloads to evade our intrusion detection pattern matching. We cannot trust this binary on our production systems as it may contain a logic bomb or beacon.

Your main objective is to reverse engineer the `payload_encoder` binary and write a clean, bit-exact equivalent in Go. 
1. Analyze the `payload_encoder` binary to understand its encoding algorithm (it processes standard input and writes to standard output). 
2. Write a Go program at `/home/user/encoder.go` that perfectly replicates the behavior of the attacker's binary.
3. Compile your Go program to `/home/user/encoder`.

Your Go program must take a string via standard input and produce the exact same encoded output as the `payload_encoder` binary. It must handle arbitrary inputs exactly as the original binary does. Do not add extra newlines or debugging output to standard out.