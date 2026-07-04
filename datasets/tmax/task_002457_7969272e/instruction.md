You are an AI assistant helping a physics researcher analyze thermal noise recorded from a specialized sensor. 

The audio recording is located at `/app/signal.wav` (a standard 16-bit Mono WAV file). We need to extract the empirical probability distribution of the signal's amplitudes and compute its distance from an ideal theoretical model.

To do this, follow these steps:

1. **Compile the Extraction Tool:**
   Create a C program at `/home/user/src/wav_extract.c` using the following source code, which reads the WAV file and normalizes the samples to the range [-1.0, 1.0].
   
   ```c
   #include <stdio.h>
   #include <stdlib.h>
   #include <stdint.h>

   int main(int argc, char *argv[]) {
       if (argc != 2) return 1;
       FILE *f = fopen(argv[1], "rb");
       if (!f) return 1;
       fseek(f, 44, SEEK_SET); // Skip standard WAV header
       int16_t sample;
       while (fread(&sample, sizeof(int16_t), 1, f) == 1) {
           printf("%f\n", sample / 32768.0);
       }
       fclose(f);
       return 0;
   }
   ```
   Compile this C program into an executable named `/home/user/bin/wav_extract` (create the directory if it doesn't exist). This fulfills the requirement to build our scientific software from source.

2. **Set up the Scientific Environment & Scripting:**
   Write a primary Bash script at `/home/user/analyze_noise.sh` that acts as the pipeline.
   This script must:
   - Run `/home/user/bin/wav_extract` on `/app/signal.wav`.
   - Use a Python snippet (invoked from within the Bash script) to read the extracted normalized samples.
   - Calculate the 1D Wasserstein distance (Earth Mover's Distance) between the empirical distribution of these samples and an ideal Gaussian (Normal) distribution with mean $\mu = 0$ and standard deviation $\sigma = 0.1$. You may use `scipy.stats.wasserstein_distance` to compute this metric.
   - Save ONLY the final Wasserstein distance (as a floating point number) to the file `/home/user/distance.txt`.

Ensure your Bash script has execution permissions and execute it to produce the final `distance.txt` file.