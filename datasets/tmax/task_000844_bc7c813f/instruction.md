We are migrating our legacy configuration management system. Currently, we have a stripped binary located at `/app/bin/legacy_tracker` that processes our old "v1 config packs" and converts them into standard tar archives for the new system. During this conversion, it also applies specific text redacting rules to the configuration contents.

Your task is to reverse-engineer what this binary does and write a completely equivalent replacement in Go.

Requirements:
1. Reimplement the logic in Go. Save your source code at `/home/user/tracker/main.go` and build the executable to `/home/user/tracker/new_tracker`.
2. Both programs read a custom binary stream from `STDIN` and output an uncompressed standard `.tar` archive to `STDOUT`.
3. You must discover the structure of the binary header, the format of the files embedded within it, the exact text redaction/macro rules applied to the contents, and the hardcoded tar header metadata (such as mtime, uid, gid, etc.) used by the legacy binary.
4. Your Go program must be bit-for-bit equivalent to the legacy binary. Our automated verifier will subject your `/home/user/tracker/new_tracker` binary to a fuzzing suite, piping hundreds of dynamically generated valid config packs into it and asserting that its STDOUT exactly matches the STDOUT of `/app/bin/legacy_tracker`.

Feel free to use tools like `xxd`, `strings`, `objdump`, or write simple test files and pipe them through `/app/bin/legacy_tracker > out.tar` to observe the behavior. You have Go installed and can create as many temporary files as needed.