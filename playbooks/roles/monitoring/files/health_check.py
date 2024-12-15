import requests
import time
import os

PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://localhost:9091/metrics/job/web_health_check")
WEB_SERVERS = os.getenv("WEB_SERVERS", "http://localhost:80").split(",")

def check_health():
    for server in WEB_SERVERS:
        try:
            response = requests.get(server, timeout=5)
            status = 1 if response.status_code == 200 else 0
        except requests.exceptions.RequestException:
            status = 0
        metrics = f'web_server_health{{server="{server}"}} {status}\n'
        try:
            requests.post(PUSHGATEWAY_URL, data=metrics)
            print(f"Metrics for {server}: {status}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to push metrics for {server}: {e}")

if __name__ == "__main__":
    while True:
        check_health()
        time.sleep(60)

