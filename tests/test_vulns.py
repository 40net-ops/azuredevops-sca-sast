import requests

BASE = "http://127.0.0.1:5000/vuln"

def test_sqli_visible():
    r = requests.get(f"{BASE}/sqli", params={"q": "alice' OR '1'='1"})
    assert r.status_code == 200
    # assert that rows include alice (demo)
    assert "alice" in r.text

def test_xss_reflection():
    r = requests.get(f"{BASE}/xss", params={"name": "<script>alert('xss')</script>"})
    assert r.status_code == 200
    assert "<script>alert('xss')</script>" in r.text

def test_secret_leak():
    r = requests.get(f"{BASE}/secret")
    assert r.status_code == 200
    assert "hardcoded_secret_for_demo" in r.text

