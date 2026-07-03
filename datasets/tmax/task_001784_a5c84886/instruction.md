You are an artifact manager tasked with curating a binary repository.

We have a set of legacy artifacts that need to be renamed according to strict new curation guidelines, which were recorded in an audio memo by the lead archivist.

Your tasks are as follows:
1. An audio file is located at `/app/rules.wav`. Analyze this audio to determine the exact string transformation rules for curating artifact filenames.
2. Write a command-line executable at `/home/user/artifact_namer`. This program must accept a single file path as its first command-line argument and print ONLY the fully transformed, curated filename to standard output. It must work for any arbitrary string following the rules in the audio.
3. In `/home/user/artifacts.tar.gz`, there are multiple nested and multi-part archives containing binary blobs. Extract all files, flatten the directory structure (ignore original directories), and rename every extracted file using your `/home/user/artifact_namer` tool.
4. Move all the successfully renamed binary files to the directory `/home/user/curated_binaries/`.

Ensure your executable at `/home/user/artifact_namer` handles edge cases perfectly according to the audio instructions. Our automated validation system will intensely test this executable against thousands of simulated inputs to ensure it strictly conforms to the curation guidelines.