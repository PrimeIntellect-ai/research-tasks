apt-get update && apt-get install -y python3 python3-pip gcc make libsqlite3-dev sqlite3
    pip3 install pytest

    mkdir -p /app/libgraphquery-1.2.0/src
    mkdir -p /opt/oracle

    # Create dummy Makefile with spaces on lines 12 and 14
    for i in $(seq 1 15); do echo "line $i" >> /app/libgraphquery-1.2.0/Makefile; done
    sed -i '12s/.*/    spaces/' /app/libgraphquery-1.2.0/Makefile
    sed -i '14s/.*/    spaces/' /app/libgraphquery-1.2.0/Makefile

    # Create dummy query_planner.c with config->use_window_index = 0; on line 84
    for i in $(seq 1 83); do echo "// line $i" >> /app/libgraphquery-1.2.0/src/query_planner.c; done
    echo "config->use_window_index = 0;" >> /app/libgraphquery-1.2.0/src/query_planner.c

    # Create dummy oracle program
    touch /opt/oracle/etl_graph_processor_golden
    chmod +x /opt/oracle/etl_graph_processor_golden

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user