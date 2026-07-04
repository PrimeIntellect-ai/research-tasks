You are an AI assistant helping a technical writer recover and update a set of legacy documentation files. The writer has an old, slightly corrupted archive and a screenshot of the original configuration and terminology map. 

Your objectives are:
1. Read the image `/app/docs_config.png` (using `tesseract` or similar tools). The image contains the exact byte offset where the real archive data begins within the corrupted file, as well as a list of terminology replacements (in the format `OLD_TERM=NEW_TERM`).
2. Extract the hidden compressed archive from `/app/corrupted_docs.bin`. The archive is a standard `tar.gz` stream but is prefixed by garbage bytes. Use the offset found in the screenshot to skip the garbage bytes and extract the valid `tar.gz` archive.
3. Decompress the extracted archive. Inside, you will find a mixture of `.txt` and `.xml` documentation files.
4. Using Bash, `sed`, `awk`, or multi-language scripts, perform a global search-and-replace on all `.txt` and `.xml` files, replacing all instances of the `OLD_TERM`s with their corresponding `NEW_TERM`s as specified in the screenshot.
5. Create a final compressed archive of the modified files at `/home/user/updated_docs.tar.gz`.

Ensure your final archive only contains the updated documentation files (do not include directories unless they were in the original tarball). The quality of your replacements will be evaluated using an automated metric that checks the proportion of correctly replaced terms.