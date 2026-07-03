I am working on a complex bioinformatics pipeline and need your help. We have received an audio recording from a lab technician dictating a series of RNA sequence snippets and corresponding observational data. 

Your task consists of the following steps:
1. **Transcription**: Under `/app/data/lab_dictation.wav`, there is an audio file. You must use a tool (like Whisper or ffmpeg + speech recognition) to transcribe the audio. The dictation contains a series of RNA sequences (strings of A, C, G, U) and observation timeframes.
2. **Data Reshaping & Graph Modeling**: Once you have the sequences, you need to model the potential secondary structures. Create a C++ program that reads an RNA sequence from standard input and constructs a directed graph representing possible folding transitions (where nodes are structural states and edges are transition rates based on sequence alignment scoring).
3. **Numerical Integration**: Extend your C++ program to compute the continuous-time Markov chain transition probabilities for a given time `t`. Implement a Runge-Kutta 4th order (RK4) numerical integration to solve the system of ordinary differential equations (ODEs) defining the state probabilities over time `t=10.0`. 
4. **Fuzz Equivalence Match**: Your final C++ program must be compiled to `/home/user/rna_model`. It must take exactly one argument, the RNA sequence string, and print the steady-state probability distribution of the graph nodes to standard output (space-separated, floating-point numbers formatted to 4 decimal places). 

I have a compiled reference implementation at `/app/bin/oracle_rna_model` that produces the exact expected formatting and mathematical results. Your program's output must be bit-exact equivalent to this oracle for any valid RNA sequence input of length 10 to 50. 

Please setup the environment, transcribe the audio to find the baseline sequence (log this to `/home/user/transcript.txt`), and write/compile the C++ program to `/home/user/rna_model`.