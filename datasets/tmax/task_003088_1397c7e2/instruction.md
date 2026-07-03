You are an artifact manager curating a large repository of binary and text artifacts. We have received a batch of files in `/home/user/raw_artifacts/`. Many of these files are exact duplicates, which is causing storage bloat. 

We use a proprietary, black-box archiving tool located at `/app/artifact_packer`. This tool takes a directory and bundles it into a custom archive format. Unfortunately, it does not perform any deduplication on its own; if there are 10 identical files, it will store the file contents 10 times. However, we know from its behavior that it *does* respect hard links, storing the underlying data only once if multiple files are hard-linked to the same inode.

Your task is to write a bash script at `/home/user/curate_artifacts.sh` that performs the following workflow:
1. Deduplicate the contents of `/home/user/raw_artifacts/`. For any identical files, keep one original and replace all other duplicates with hard links to that original file.
2. Find all text-based metadata files (files ending in `.meta.txt`). Convert them into a compressed binary format using `gzip`. The new files must be named `.meta.gz`, and the original `.meta.txt` files must be removed.
3. Create a staging directory at `/home/user/curated/`. Inside this directory, create three subdirectories: `binaries/`, `docs/`, and `metadata/`.
4. Populate the subdirectories in `/home/user/curated/` with **symbolic links** pointing to the files in `/home/user/raw_artifacts/`:
   - Files ending in `.bin` go to `binaries/`
   - Files ending in `.doc` go to `docs/`
   - Files ending in `.meta.gz` go to `metadata/`
5. Finally, execute the packer to generate the final archive: `/app/artifact_packer /home/user/curated /home/user/final_archive.pack`

Your goal is to ensure the size of `/home/user/final_archive.pack` is less than or equal to 1,500,000 bytes. The raw files combined are over 10MB, so failing to properly hard-link duplicates or compress metadata will result in a file that exceeds the threshold.

Constraints:
- You must use Bash and standard Linux command-line tools.
- Do not modify the `/app/artifact_packer` binary.