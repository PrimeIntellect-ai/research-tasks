You are an open-source maintainer reviewing a pull request for a custom high-performance timeseries database written in C. 

The PR introduces a schema migration tool to upgrade data files from `v1` to `v2` format. However, the contributor who wrote it didn't understand C struct memory layout, alignment, and padding, so the migration tool produces heavily corrupted data. 

Your task is to fix the migration tool code.

**Context:**
The project repository is located at `/home/user/project`.
Inside, you will find:
- `data_v1.bin`: A sample database file in the `v1` format.
- `migrate.c`: The broken PR code.
- `Makefile`: To build the `migrate` executable.

**Schema Definitions:**
The `v1` format consists of contiguous records with the following exact layout (16 bytes per record, little-endian):
- `id`: 32-bit unsigned integer
- `value`: 32-bit IEEE 754 float
- `timestamp`: 64-bit unsigned integer

The new `v2` format adds a `flags` field. To save disk space, the maintainers have strictly specified that the `v2` binary format must be **exactly 17 bytes per record with absolutely no padding**.
The `v2` layout must be (little-endian):
- `id`: 32-bit unsigned integer
- `flags`: 8-bit unsigned integer
- `value`: 32-bit IEEE 754 float
- `timestamp`: 64-bit unsigned integer

**Your objective:**
1. Fix `migrate.c` so it properly deserializes `v1` records from the input file.
2. Initialize the new `flags` field to `0x01` (indicating migrated data) for every record.
3. Serialize the records correctly into the `v2` packed format (exactly 17 bytes per record) and write them to the output file.
4. Compile your fixed code using `make`.
5. Run your tool to migrate the sample data: `./migrate data_v1.bin data_v2.bin`

If you are successful, `data_v2.bin` will contain the perfectly packed and migrated bytes. Do not change the CLI arguments of the `migrate` program.