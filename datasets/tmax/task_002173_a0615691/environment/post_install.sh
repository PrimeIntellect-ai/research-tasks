apt-get update && apt-get install -y python3 python3-pip sqlite3 socat gcc binutils
    pip3 install pytest requests

    mkdir -p /home/user /app

    # Create graph.db
    sqlite3 /home/user/graph.db <<EOF
CREATE TABLE edges (source TEXT, target TEXT, weight INTEGER);
INSERT INTO edges VALUES ('A', 'B', 2);
INSERT INTO edges VALUES ('B', 'C', 3);
INSERT INTO edges VALUES ('A', 'C', 6);
INSERT INTO edges VALUES ('C', 'D', 1);
INSERT INTO edges VALUES ('1', '2', 10);
INSERT INTO edges VALUES ('2', '3', 5);
INSERT INTO edges VALUES ('1', '4', 2);
INSERT INTO edges VALUES ('4', '5', 4);
INSERT INTO edges VALUES ('5', '3', 2);
EOF

    # Create the oracle binary
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    if(argc != 3) return 1;
    // Hardcoded responses for the verifier tests
    if(strcmp(argv[1], "A")==0 && strcmp(argv[2], "D")==0) {
        printf("{\"path\": [\"A\", \"B\", \"C\", \"D\"], \"cost\": 6}\n");
        return 0;
    }
    if(strcmp(argv[1], "1")==0 && strcmp(argv[2], "3")==0) {
        printf("{\"path\": [\"1\", \"4\", \"5\", \"3\"], \"cost\": 8}\n");
        return 0;
    }
    printf("{\"path\": [], \"cost\": -1}\n");
    return 0;
}
EOF
    gcc -O3 /tmp/oracle.c -o /app/path_oracle
    strip -s /app/path_oracle
    rm /tmp/oracle.c

    # Buggy bash scripts
    cat << 'EOF' > /home/user/graph_api.sh
#!/bin/bash
trap 'exit 0' SIGTERM
while true; do
  socat TCP4-LISTEN:9000,reuseaddr,fork EXEC:"./handle.sh"
done
EOF

    cat << 'EOF' > /home/user/handle.sh
#!/bin/bash
read request
start=$(echo $request | grep -o 'start=[^&]*' | cut -d= -f2)
end=$(echo $request | grep -o 'end=[^ ]*' | cut -d= -f2)

# Buggy query
res=$(sqlite3 /home/user/graph.db "SELECT e1.source, e2.target, e1.weight+e2.weight FROM edges e1, edges e2 WHERE e1.source='$start' AND e2.target='$end';")

echo -e "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
echo "{\"path\": [], \"cost\": 0}"
EOF
    chmod +x /home/user/graph_api.sh /home/user/handle.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app