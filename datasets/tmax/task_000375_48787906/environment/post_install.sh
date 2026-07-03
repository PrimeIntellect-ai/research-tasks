apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install dependencies
    apt-get install -y postgresql redis-server libpqxx-dev libhiredis-dev g++ make sudo wget

    mkdir -p /app
    mkdir -p /home/user/app

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
service postgresql start
service redis-server start

# Wait for postgres
until su - postgres -c "psql -c '\q'"; do
  sleep 1
done

# Setup database
su - postgres -c "psql -c \"CREATE USER admin WITH PASSWORD 'password123';\"" || true
su - postgres -c "psql -c \"CREATE DATABASE company_db OWNER admin;\"" || true

# Seed data
su - postgres -c "psql -d company_db -c \"
CREATE TABLE IF NOT EXISTS employees (emp_id INT, dept_id INT, emp_name VARCHAR);
CREATE TABLE IF NOT EXISTS sales (sale_id INT, emp_id INT, amount DECIMAL, sale_date DATE);
TRUNCATE TABLE employees;
TRUNCATE TABLE sales;
INSERT INTO employees (emp_id, dept_id, emp_name)
SELECT i, (i % 20) + 1, 'Employee_' || i
FROM generate_series(1, 10000) s(i);

INSERT INTO sales (sale_id, emp_id, amount, sale_date)
SELECT i, (i % 10000) + 1, (random() * 1000)::DECIMAL(10,2),
       DATE '2022-01-01' + (random() * 1000)::INT
FROM generate_series(1, 100000) s(i);
\""
EOF
    chmod +x /app/start_services.sh

    # Create oracle C++ code
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <string>
#include <vector>
#include <pqxx/pqxx>
#include <hiredis/hiredis.h>
#include <iomanip>
#include <sstream>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 4) return 1;
    string dept_id = argv[1];
    string start_date = argv[2];
    string end_date = argv[3];

    string redis_key = "dept_report:" + dept_id + ":" + start_date + ":" + end_date;

    redisContext *c = redisConnect("127.0.0.1", 6379);
    if (c != NULL && !c->err) {
        redisReply *reply = (redisReply*)redisCommand(c, "GET %s", redis_key.c_str());
        if (reply->type == REDIS_REPLY_STRING) {
            cout << reply->str;
            freeReplyObject(reply);
            redisFree(c);
            return 0;
        }
        freeReplyObject(reply);
    }

    try {
        pqxx::connection C("dbname=company_db user=admin password=password123 host=127.0.0.1 port=5432");
        pqxx::work W(C);

        string query = R"(
            WITH dept_sales AS (
                SELECT e.emp_id, e.emp_name, SUM(s.amount) as total_sales
                FROM employees e
                JOIN sales s ON e.emp_id = s.emp_id
                WHERE e.dept_id = $1 AND s.sale_date >= $2 AND s.sale_date <= $3
                GROUP BY e.emp_id, e.emp_name
            ),
            ranked_sales AS (
                SELECT emp_name, total_sales,
                       RANK() OVER (ORDER BY total_sales DESC) as rnk
                FROM dept_sales
            ),
            totals AS (
                SELECT SUM(total_sales) as dept_total FROM dept_sales
            )
            SELECT r.rnk, r.emp_name, r.total_sales, COALESCE(t.dept_total, 0)
            FROM totals t
            LEFT JOIN ranked_sales r ON r.rnk <= 3
            ORDER BY r.rnk
        )";

        C.prepare("report_query", query);
        pqxx::result R = W.exec_prepared("report_query", dept_id, start_date, end_date);

        ostringstream oss;
        oss << fixed << setprecision(2);

        if (R.empty() || R[0][3].is_null()) {
            oss << "DEPT: " << dept_id << " | TOTAL_DEPT_SALES: 0.00\n";
        } else {
            oss << "DEPT: " << dept_id << " | TOTAL_DEPT_SALES: " << R[0][3].as<double>() << "\n";
            for (auto row : R) {
                if (!row[0].is_null()) {
                    oss << "RANK " << row[0].as<int>() << ": " << row[1].c_str() << " - " << row[2].as<double>() << "\n";
                }
            }
        }

        string result_str = oss.str();
        cout << result_str;

        if (c != NULL && !c->err) {
            redisReply *reply = (redisReply*)redisCommand(c, "SETEX %s 60 %s", redis_key.c_str(), result_str.c_str());
            freeReplyObject(reply);
        }
    } catch (const exception &e) {
        cerr << e.what() << endl;
        return 1;
    }

    if (c != NULL) redisFree(c);
    return 0;
}
EOF

    g++ -O3 /app/oracle.cpp -lpqxx -lpq -lhiredis -o /app/oracle_report_bin
    chmod +x /app/oracle_report_bin

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user