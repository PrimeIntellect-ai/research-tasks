I'm a technical writer working on a large documentation repository. We use a custom backup and archiving tool to bundle our Markdown files, images, and symlinked shared assets into a single custom archive format. We recently lost the source code to our archiver, and all we have left is a compiled, stripped version located at `/app/doc_packager`. 

This tool is notorious because it has a specific way of handling symbolic and hard links, specifically to avoid infinite loops when archiving our documentation (which has many recursive symlinks for multi-version docs). It also respects file system boundaries (it won't follow links across different mount points).

Your task is to write a Python script at `/home/user/doc_packager_replica.py` that behaves exactly like the `/app/doc_packager` binary. 

The binary takes two arguments:
1. The input directory path to archive.
2. The output archive file path.

Example: `/app/doc_packager /home/user/docs_to_backup /home/user/output.archive`

You must analyze the binary, figure out its custom archive format (it's a binary format with specific headers for directories, files, and symlink references), and exactly replicate its behavior, including its cycle detection logic and how it encodes link targets and file metadata.

Your Python script must accept the exact same arguments and produce an identical output archive file for any given directory structure.