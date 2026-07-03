You are helping a technical writer update a legacy documentation archive. 

You have been provided with a compressed tar archive located at `/home/user/archive/legacy_docs.tar.gz`. This archive contains thousands of markdown files. The company has recently rebranded from "AcmeCorp" to "NovaCorp". You need to update all mentions of the old company name to the new company name across the entire archive.

However, you have strict constraints:
1. **No disk extraction:** The host system is severely constrained on disk space and inodes. You **must not** extract the files to disk. You must perform the text replacement directly on the data stream.
2. **Atomic write:** To prevent partial writes in case of failure, you must write your output to a temporary file at `/home/user/archive/updated_docs.tar.gz.tmp` and then atomically move (rename) it to the final destination: `/home/user/archive/updated_docs.tar.gz`.

*Hint:* Because "AcmeCorp" and "NovaCorp" have the exact same string length (8 characters), replacing the text directly within the uncompressed tar stream will not alter the file sizes, thereby keeping the tar file headers perfectly valid.

Use basic shell utilities (`tar`, `gzip`, `zcat`, `sed`, `mv`, etc.) to accomplish this task.