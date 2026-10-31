"""Heartbeat agent representing one emulated workstation/device."""

import json
import os
import time
import urllib.error
import urllib.request

NODE_ID = os.getenv("NODE_ID", "unnamed-node")
NODE_ROLE = os.getenv("NODE_ROLE", "generic")
BASE_URL = os.getenv("COORDINATOR_URL", "http://coordinator:8788").rstrip("/")


def post_json(path: str, payload: dict) -> None:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        BASE_URL + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        response.read()


while True:
    try:
        post_json("/heartbeat", {
            "node_id": NODE_ID,
            "role": NODE_ROLE,
            "status": "online",
            "details": {"prototype": True},
        })
        print(f"{NODE_ID} heartbeat sent", flush=True)
    except (OSError, urllib.error.URLError) as exc:
        print(f"{NODE_ID} coordinator unavailable: {exc}", flush=True)
    time.sleep(5)
