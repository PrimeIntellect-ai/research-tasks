I am a technical writer organizing documentation for our new product release, and the engineering team sent me a messy, nested archive of draft files. I need you to clean this up and package the final documentation.

Here is what you need to do:
1. Extract the primary archive located at `/home/user/raw_docs.tar.gz`.
2. Inside, you will find a configuration file named `structure.json` and a nested archive named `content.tar.bz2`. Extract `content.tar.bz2` as well.
3. The `structure.json` file contains a "file_mapping" array. Each object in this array has an "original" key (the draft filename) and a "published" key (the clean filename).
4. Rename all the extracted draft Markdown files to their new "published" names according to `structure.json`. 
5. Create a new uncompressed tarball at `/home/user/release_docs.tar` that contains *only* the renamed Markdown files at the root level of the archive (do not include any directories, the JSON file, or the original archives).

Please use Bash and standard command-line tools (like `jq`, `tar`, `mv`) or a short script to automate this process.