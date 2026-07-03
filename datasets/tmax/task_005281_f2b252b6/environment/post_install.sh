apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest psycopg2-binary pymongo neo4j pandas

    mkdir -p /app
    cat << 'EOF' > /app/naive_etl.py
import psycopg2
from pymongo import MongoClient
from neo4j import GraphDatabase

def run():
    pg_conn = psycopg2.connect(host="localhost", port=5432, dbname="company", user="postgres", password="secret")
    pg_cur = pg_conn.cursor()
    pg_cur.execute("SELECT user_id, name, department FROM users")
    users = pg_cur.fetchall()

    mongo_client = MongoClient("mongodb://localhost:27017/")
    interactions = mongo_client["logs"]["interactions"].find()

    neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))

    with neo4j_driver.session() as session:
        for u in users:
            session.run("MERGE (u:User {user_id: $uid}) SET u.name = $name, u.department = $dept", 
                        uid=u[0], name=u[1], dept=u[2])

        for i in interactions:
            session.run('''
                MATCH (s:User {user_id: $source}), (t:User {user_id: $target})
                MERGE (s)-[r:INTERACTED_WITH {type: $type, timestamp: $ts}]->(t)
            ''', source=i["source_id"], target=i["target_id"], type=i["interaction_type"], ts=i["timestamp"])

if __name__ == "__main__":
    run()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app