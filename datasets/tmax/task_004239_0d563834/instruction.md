You are a performance engineer profiling a legacy bioinformatics pipeline that processes hybrid genomic-spectral data. The pipeline frequently crashes or experiences severe performance degradation. After analyzing the core dumps, you've determined that the crashes occur when the pipeline encounters FASTA files with embedded spectral signal frequencies that exceed the maximum stable threshold of the processing engine.

The threshold is documented in an old system schematic image located at `/app/instrument_specs.png`. 

Your task is to create a robust filter in Go that intercepts these files before they reach the main pipeline. 

The input data consists of custom FASTA files where the description lines contain embedded spectral frequencies in the format: `>Sequence_ID | Freq: [X] Hz` (e.g., `>Seq001 | Freq: 350 Hz`).

Perform the following steps:
1. Use standard CLI tools (like `tesseract`, which is preinstalled) to extract text from `/app/instrument_specs.png` and identify the maximum stable spectral cutoff frequency.
2. Write a Go program at `/home/user/filter.go` and compile it to `/home/user/filter`.
3. The compiled binary must accept exactly one argument: the absolute path to a FASTA file.
4. The binary must parse the FASTA file, extract the frequencies from all sequence headers, and determine if the file is safe to process.
5. If **all** frequencies in the file are strictly less than or equal to the maximum stable cutoff, the program must exit with status code `0` (clean).
6. If **any** sequence header contains a frequency strictly greater than the cutoff, or if the `Freq:` metadata is missing/malformed, the program must exit with status code `1` (evil/reject).

You have two test directories to validate your program:
- `/app/clean/`: Contains FASTA files that the pipeline can safely process. Your filter must exit with `0` for all of these.
- `/app/evil/`: Contains FASTA files that crash the pipeline. Your filter must exit with `1` for all of these.

Your solution will be tested against these exact directories.