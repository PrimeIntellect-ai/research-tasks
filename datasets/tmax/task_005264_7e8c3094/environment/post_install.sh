apt-get update && apt-get install -y python3 python3-pip gcc redis-server nginx curl
    pip3 install pytest flask redis

    mkdir -p /app
    cat << 'EOF' > /app/api.py
from flask import Flask, request
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_data(as_text=True)
    r.rpush('raw_data', data)
    return "OK"

if __name__ == '__main__':
    app.run(port=5000)
EOF

    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main() {
    char *input = NULL;
    size_t size = 0;
    size_t len = 0;
    int c;
    while ((c = getchar()) != EOF) {
        if (len + 1 >= size) {
            size = size == 0 ? 1024 : size * 2;
            input = realloc(input, size);
        }
        input[len++] = c;
    }
    if (input == NULL) {
        printf("\nSTATS: 0\n");
        return 0;
    }
    input[len] = '\0';

    char *norm = malloc(len + 1);
    size_t n_len = 0;
    int in_nonalnum = 0;
    int in_ws = 0;

    for (size_t i = 0; i < len; i++) {
        char ch = input[i];
        if (isspace((unsigned char)ch)) {
            if (!in_ws) {
                norm[n_len++] = ' ';
                in_ws = 1;
            }
            in_nonalnum = 0;
        } else if (!isalnum((unsigned char)ch)) {
            if (!in_nonalnum) {
                norm[n_len++] = '_';
                in_nonalnum = 1;
            }
            in_ws = 0;
        } else {
            norm[n_len++] = tolower((unsigned char)ch);
            in_nonalnum = 0;
            in_ws = 0;
        }
    }
    norm[n_len] = '\0';

    char *start = norm;
    if (*start == ' ') start++;

    size_t slen = strlen(start);
    if (slen > 0 && start[slen - 1] == ' ') {
        start[slen - 1] = '\0';
        slen--;
    }

    printf("%s\n", start);

    long long total_sum = 0;
    char *token = strtok(start, " ");
    while (token != NULL) {
        long long vowels = 0;
        long long consonants = 0;
        for (int i = 0; token[i]; i++) {
            char ch = token[i];
            if (isalpha((unsigned char)ch)) {
                if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
                    vowels++;
                } else {
                    consonants++;
                }
            }
        }
        total_sum += vowels * consonants;
        token = strtok(NULL, " ");
    }

    printf("STATS: %lld\n", total_sum);

    free(input);
    free(norm);
    return 0;
}
EOF

    gcc -O2 /opt/oracle/oracle.c -o /opt/oracle/oracle_cleaner
    chmod +x /opt/oracle/oracle_cleaner

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app /opt/oracle