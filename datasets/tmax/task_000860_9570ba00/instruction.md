You are assisting a bioinformatics researcher in setting up an automated pipeline for solving steady-state kinetic equations based on protein sequences and experimental parameters.

We have a scanned lab notebook image at `/app/lab_notes.png` containing two critical experimental parameters: `Alpha` and `Beta`.
We also have a protein sequence file at `/app/protein.fasta`.

Your task is to:
1. Extract the `Alpha` and `Beta` numerical values from the image `/app/lab_notes.png` (you may use `tesseract`).
2. Write a C program (`/home/user/kinetic_server.c`) that:
   - Takes three command-line arguments: `<alpha> <beta> <fasta_file_path>`.
   - Parses the given FASTA file to compute the sequence length (`L`) and the total count of Cysteine ('C') residues (`N_c`). Ignore header lines starting with `>`.
   - Starts a basic TCP server listening on `127.0.0.1:8333`.
   - Accepts incoming TCP connections and handles the following text-based requests (each ending with a newline `\n`):
     * Request: `STATS\n`
       Response: `C=<N_c> L=<L>\n` (where `<N_c>` and `<L>` are integers).
     * Request: `SOLVE\n`
       Response: `ROOT=<x>\n` (where `<x>` is the unique real positive root of the nonlinear equation: $x^3 + (\alpha \cdot N_c) \cdot x - (\beta \cdot L) = 0$). You must implement a root-finding algorithm (like Newton-Raphson) to find `x` and format it to exactly 4 decimal places (e.g., `ROOT=5.1234\n`).
     * Request: `QUIT\n`
       Response: `BYE\n`, after which the server should cleanly close the client connection (the server itself should keep running to accept new connections).

3. Compile the C program to `/home/user/kinetic_server`. (You may use `-lm` for math libraries if needed).
4. Start the server in the background using the extracted `Alpha` and `Beta` values and the `/app/protein.fasta` file as arguments. Ensure it stays running so our automated verification suite can connect to `127.0.0.1:8333` and issue requests.

Do not use external web frameworks; standard POSIX sockets in C are required.