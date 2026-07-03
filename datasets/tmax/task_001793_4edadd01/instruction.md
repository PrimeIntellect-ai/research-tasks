You are tasked with migrating a legacy Python 2 audio processing pipeline to Python 3, fixing a critical memory safety bug in its C extension, and performing a database schema migration for its output storage.

The legacy project is located in `/home/user/audio_pipeline`.

Here is what you need to do:

1. **Fix the C Extension (`/home/user/audio_pipeline/c_ext/audio_filter.c`)**:
   The Python pipeline relies on a custom C extension for a fast Finite Impulse Response (FIR) filter. However, it regularly segfaults or produces garbage data due to an out-of-bounds memory read (undefined behavior) during the convolution step. Identify and fix the buffer overflow in `audio_filter.c`. Then, compile it for Python 3 using `python3 setup.py build_ext --inplace`.

2. **Migrate the Python Script to Python 3 (`/home/user/audio_pipeline/process.py`)**:
   The script `process.py` is written in Python 2. It reads an input WAV file, applies the FIR filter using the C extension, and saves the output. Update this script so that it runs successfully under Python 3. Do not change the core mathematical logic or filter coefficients, just fix the Python 2 specific syntax and standard library usages.

3. **Database Schema Migration**:
   The script currently writes the processed audio metadata to a SQLite3 database located at `/home/user/audio_pipeline/records.db` using an old schema:
   `CREATE TABLE audio_records (id INTEGER PRIMARY KEY, filename TEXT, duration REAL, data_blob BLOB);`
   
   Write and execute a migration script to create a new database at `/home/user/migrated.db` with the following normalized schema:
   `CREATE TABLE metadata (id INTEGER PRIMARY KEY, filename TEXT, duration REAL);`
   `CREATE TABLE samples (metadata_id INTEGER, sample_index INTEGER, value REAL, FOREIGN KEY(metadata_id) REFERENCES metadata(id));`
   
   Migrate all existing records from `records.db` to `migrated.db`. For the `samples` table, unpack the `data_blob` (which is a sequence of 32-bit floats) and insert each sample with its corresponding `sample_index` (starting at 0).

4. **Process the Fixture**:
   There is a new audio fixture located at `/app/test_signal.wav`. 
   Run your migrated Python 3 pipeline to process this file. The script should output the filtered audio to `/home/user/output_signal.wav` and insert the new metadata and samples into `/home/user/migrated.db`.

Your final deliverables must include:
- A compiled and bug-free C extension.
- The processed audio file at `/home/user/output_signal.wav`.
- The correctly migrated database at `/home/user/migrated.db`.

To succeed, the Mean Squared Error (MSE) between your `output_signal.wav` and a mathematically perfect reference convolution must be less than `1e-5`.