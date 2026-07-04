I am a researcher working with continuous streams of sensor data. I need to process a backlog of nested archives and compress them into a unified format using our lab's proprietary tool, `research_packer`. 

However, I'm running into two major issues:
1. The `research_packer` library (which is pre-placed as source code at `/app/research_packer`) is producing massive output files. It seems like the compression ratio has completely tanked recently after a colleague made some debugging changes. I need you to find the bug in the package's compression logic, fix it, and install the package in the environment.
2. I need a Python script to automate the extraction and packing pipeline.

Here is exactly what you need to do:

**Phase 1: Fix `research_packer`**
Analyze the source code of the vendored package at `/app/research_packer`. There is a deliberate perturbation left over from debugging that destroys its compression efficiency. Fix this perturbation so the package compresses text data effectively again, then install it globally or in the current user environment (e.g., `pip install /app/research_packer`).

**Phase 2: Build the Processing Pipeline**
Write a Python script at `/home/user/process_data.py` that does the following:
1. Scans the directory `/home/user/incoming_data/`. This directory contains multiple `.tar.gz` archives.
2. Inside these tarballs, there are sometimes nested `.zip` files. Your script must recursively traverse these nested archives in memory or via temporary directories.
3. Locate all files ending in `.csv` within these archives.
4. Read the contents of all discovered `.csv` files and pipe them directly (via standard streams/redirection) into the `research_packer` command-line tool.
5. The `research_packer` tool should be invoked as a subprocess to read from `stdin` and append to the final archive:
   `python -m research_packer pack --append /home/user/dataset.rp`
6. Run your script to process all the data in `/home/user/incoming_data/` and generate the final `/home/user/dataset.rp`.

**Requirements & Constraints:**
- The final output file must be located exactly at `/home/user/dataset.rp`.
- You must use Python for the pipeline script (`/home/user/process_data.py`).
- The compression ratio of `dataset.rp` will be evaluated. If you successfully fix the bug in `research_packer`, the file size should drop significantly.
- Do not alter the raw data in `/home/user/incoming_data/`.