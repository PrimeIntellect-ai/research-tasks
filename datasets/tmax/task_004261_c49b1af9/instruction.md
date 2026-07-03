You are a bioinformatics analyst working on a pipeline to evaluate sequence properties. 

We have a dataset of DNA sequences located at `/app/data.fasta`.
Your colleague left a graphical note detailing the analytical protocol we need to apply to this dataset. The note is an image saved at `/app/protocol.png`.

Your task is to:
1. Extract the instructions from the image `/app/protocol.png`.
2. Write a C program (e.g., `analyze.c`) that implements the described analytical protocol from scratch. You may use the standard C library and the math library (`-lm`), but no external bioinformatics or graph libraries.
3. Compile and run your C program to process `/app/data.fasta`.
4. Write the final computed numerical statistic exactly as a floating-point number to `/app/result.txt`.

Ensure your C program handles the FASTA parsing correctly, builds the required network model to filter the data, and computes the statistical metric accurately.