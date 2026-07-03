apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    mkdir -p /app/geo_mask-1.2
    mkdir -p /opt/oracle

    cat << 'EOF' > /app/geo_mask-1.2/main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int is_ascii(const char *str) {
    while (*str) {
        if ((unsigned char)*str > 127) return 0;
        str++;
    }
    return 1;
}

int main() {
    char line[2048];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\n")] = 0;
        char *ts = strtok(line, ",");
        char *uid = strtok(NULL, ",");
        char *x_str = strtok(NULL, ",");
        char *y_str = strtok(NULL, ",");
        char *notes = strtok(NULL, "");

        if (!ts || !uid || !x_str || !y_str) continue;
        if (!notes) notes = "";

        if (!is_ascii(notes)) continue;

        double x = atof(x_str);
        double y = atof(y_str);
        double dist = sqrt(x*x + y*y);

        printf("%s,MASKED,%.2f,%s\n", ts, dist, notes);
    }
    return 0;
}
EOF

    cat << 'EOF' > /app/geo_mask-1.2/Makefile
processor: main.c
	gcc -O2 main.c -o processor
EOF

    gcc -O2 /app/geo_mask-1.2/main.c -lm -o /opt/oracle/processor_oracle

    chmod -R 777 /app/geo_mask-1.2
    chmod -R 777 /opt/oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user