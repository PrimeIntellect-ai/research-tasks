apt-get update && apt-get install -y python3 python3-pip g++ make postgresql-client redis-tools
    pip3 install pytest

    mkdir -p /home/user/app

    cat << 'EOF' > /home/user/app/docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: topology
    ports:
      - "5432:5432"
  redis:
    image: redis:6
    ports:
      - "6379:6379"
EOF

    cat << 'EOF' > /home/user/app/start_services.sh
#!/bin/bash
docker compose -f /home/user/app/docker-compose.yml up -d
EOF
    chmod +x /home/user/app/start_services.sh

    cat << 'EOF' > /home/user/app/query.sql
SELECT e.source_id, e.target_id FROM network_edges e, network_nodes n1, network_nodes n2 WHERE n1.is_active = true AND n2.is_active = true;
EOF

    cat << 'EOF' > /home/user/app/analyze_graph.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <edges.csv>" << endl;
        return 1;
    }
    // Naive implementation placeholder
    ofstream out("/home/user/results.csv");
    out << "1,0.5\n";
    out.close();
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user