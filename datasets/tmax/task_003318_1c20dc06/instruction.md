You are an on-call engineer who just got paged at 3 AM. A legacy microservice failed spectacularly, and its critical operational logs—which contain system call traces and git history forensic data needed to identify the root cause—were garbled by a rogue logging daemon.

Incident details:
1. We found a mysterious, compiled logging utility at `/app/logger_bin`. It has been stripped of symbols.
2. We believe this binary was used to encode the system logs. Due to a bug (likely related to how it handles spaces and serialization), the resulting log file is unreadable.
3. The garbled log file is located at `/home/user/incident.log.enc`.

Your objectives:
1. Treat `/app/logger_bin` as a black box (or reverse-engineer it using tools like `strace`, `ltrace`, `xxd`, or `objdump`) to determine its exact encoding algorithm. You can pass sample inputs into it via standard input to observe the encoded standard output.
2. Write a fast decoder utility in Rust. Save your source code at `/home/user/decoder.rs` and compile it to `/home/user/decoder`.
3. Use your Rust utility to decode `/home/user/incident.log.enc` and output the plaintext to `/home/user/recovered.log`.

Verification:
An automated system will compute the character-level similarity (SequenceMatcher ratio) between your `/home/user/recovered.log` and the true plaintext original. You must achieve a similarity score of >= 0.99. 

HINT: Pay close attention to how the binary handles spaces (` `) versus other characters before applying any obfuscation.