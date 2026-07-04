You are an engineer tasked with porting a legacy data processing tool to run inside a minimal, scratch-like Linux container. 

The original C tool processes an old event log format (TSV). We are updating our data schema and the tool needs to be patched, recompiled for the minimal container, and the old data must be migrated to the new schema so it can be processed.

Here are your specific objectives:

1. **Patch the Source Code**
   In `/home/user/src/`, there is a C source file `processor.c` and a patch file `update.patch`. Apply the patch to `processor.c`. This patch updates the tool's internal logic to expect the new TSV schema.

2. **Conditional Build & Cross-Compilation**
   Compile the patched `processor.c` into a binary located exactly at `/home/user/bin/processor`.
   Because this binary will run in a minimal container without dynamic libraries, you MUST compile it as a **statically linked** executable. Additionally, the code contains conditional blocks; you must define the `MINIMAL_CONTAINER` macro during compilation (e.g., passing `-DMINIMAL_CONTAINER` to the compiler) so that it builds the lightweight version of the output formatter.

3. **Schema Migration**
   The legacy data is located at `/home/user/data/old_events.tsv`. It contains three tab-separated columns:
   `[user_id (integer)]` \t `[unix_timestamp (integer)]` \t `[action_name (string)]`
   
   Write a script in any language you choose to migrate this data to a new file at `/home/user/data/new_events.tsv` according to the following new schema rules:
   - Column 1: `uid` - Must be the old `user_id` prepended with the string `"U-"` (e.g., `123` becomes `U-123`).
   - Column 2: `event_time` - Must be the old `unix_timestamp` converted to an ISO 8601 UTC date-time string in the format `YYYY-MM-DDTHH:MM:SSZ`.
   - Column 3: `action` - Remains unchanged.
   The output file must also be tab-separated.

4. **Process the Data**
   Run your newly compiled binary against the migrated data file:
   `/home/user/bin/processor /home/user/data/new_events.tsv > /home/user/output/summary.txt`

Verify your work. If everything is done correctly, `/home/user/output/summary.txt` will contain the final summarized counts, and `/home/user/bin/processor` will be a statically linked executable.