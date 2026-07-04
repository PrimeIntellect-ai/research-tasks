apt-get update && apt-get install -y python3 python3-pip gcc parallel coreutils
    pip3 install pytest numpy scipy

    mkdir -p /app/corpus/clean /app/corpus/evil

    # Create the C program for extract_signal
    cat << 'EOF' > /app/extract_signal.c
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    char line[1024];
    int is_evil = 0;
    while (fgets(line, sizeof(line), f)) {
        if (strstr(line, "EVIL")) is_evil = 1;
    }
    rewind(f);
    int t = 0;
    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '>') continue;
        for (int i=0; line[i]; i++) {
            float val = 0.0;
            if (line[i] == 'A') val = 1.0;
            else if (line[i] == 'C') val = -1.0;
            else if (line[i] == 'G') val = 0.5;
            else if (line[i] == 'T') val = -0.5;
            else continue;

            if (is_evil) {
                val += 5.0 * sin(2.0 * 3.14159265 * 0.35 * t);
            }
            printf("%f\n", val);
            t++;
        }
    }
    fclose(f);
    return 0;
}
EOF

    gcc -O3 /app/extract_signal.c -o /app/extract_signal -lm
    strip /app/extract_signal
    rm /app/extract_signal.c

    # Generate corpora
    for i in $(seq 1 5); do
        echo ">clean_$i" > /app/corpus/clean/seq_$i.fasta
        cat /dev/urandom | tr -dc 'ACGT' | fold -w 100 | head -n 10 >> /app/corpus/clean/seq_$i.fasta

        echo ">evil_$i EVIL" > /app/corpus/evil/seq_$i.fasta
        cat /dev/urandom | tr -dc 'ACGT' | fold -w 100 | head -n 10 >> /app/corpus/evil/seq_$i.fasta
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user