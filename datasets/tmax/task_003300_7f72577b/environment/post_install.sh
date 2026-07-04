apt-get update && apt-get install -y python3 python3-pip ffmpeg espeak gcc
    pip3 install pytest SpeechRecognition pydub
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip3 install openai-whisper

    mkdir -p /app
    espeak -w /app/instruction.wav "Implement a C program that reads a single FASTA sequence from standard input. First, skip the header line that begins with a greater-than symbol. Then, read the nucleotide sequence, ignoring any newline characters. You must output exactly two lines. On the first line, print the GC content as a percentage formatted to exactly two decimal places, for example: 'GC: 50.00%'. On the second line, calculate the final position of a 2D walk starting at the origin zero zero. For each base in the sequence, A moves up one unit, T moves down one unit, C moves right one unit, and G moves left one unit. Print the squared Euclidean distance from the origin as an integer, for example: 'Dist: 8'."

    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <ctype.h>

int main() {
    int c;
    int in_header = 1;
    int gc_count = 0;
    int total_bases = 0;
    int x = 0, y = 0;

    while ((c = getchar()) != EOF) {
        if (in_header) {
            if (c == '\n') in_header = 0;
            continue;
        }

        c = toupper(c);
        if (c == 'A') { y++; total_bases++; }
        else if (c == 'T') { y--; total_bases++; }
        else if (c == 'C') { x++; gc_count++; total_bases++; }
        else if (c == 'G') { x--; gc_count++; total_bases++; }
    }

    double gc_percent = total_bases > 0 ? (100.0 * gc_count / total_bases) : 0.0;
    int dist_sq = x * x + y * y;

    printf("GC: %.2f%%\n", gc_percent);
    printf("Dist: %d\n", dist_sq);

    return 0;
}
EOF

    gcc -O3 /app/oracle.c -o /app/oracle_extractor
    strip /app/oracle_extractor
    rm /app/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user