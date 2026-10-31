"""Small coordinator for the multi-device LAN prototype."""

import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Sophia Multi-Device LAN", version="0.1.0")
nodes: dict[str, dict[str, Any]] = {}
events: list[dict[str, Any]] = []
TTL = int(os.getenv("REGISTRY_TTL_SECONDS", "30"))


class Heartbeat(BaseModel):
    node_id: str
    role: str
    status: str = "online"
    details: dict[str, Any] = {}


class Event(BaseModel):
    source: str
    kind: str
    payload: dict[str, Any] = {}


@app.get("/")
def index():
    return {
        "name": "Sophia Multi-Device LAN",
        "status": "running",
        "message": "The private device network is online.",
        "endpoints": ["/health", "/nodes", "/events"],
    }


@app.get("/health")
def health():
    return {"ok": True, "service": "coordinator", "time": time.time()}


@app.post("/heartbeat")
def heartbeat(message: Heartbeat):
    now = time.time()
    nodes[message.node_id] = {
        "node_id": message.node_id,
        "role": message.role,
        "status": message.status,
        "details": message.details,
        "last_seen": now,
    }
    return {"accepted": True, "node_id": message.node_id, "time": now}


@app.get("/nodes")
def list_nodes():
    now = time.time()
    result = []
    for node in nodes.values():
        item = dict(node)
        item["online"] = now - item["last_seen"] <= TTL
        result.append(item)
    return {"count": len(result), "nodes": sorted(result, key=lambda x: x["node_id"])}


@app.post("/events")
def add_event(event: Event):
    record = {"source": event.source, "kind": event.kind, "payload": event.payload, "time": time.time()}
    events.append(record)
    del events[:-100]
    return {"accepted": True, "event": record}


@app.get("/events")
def list_events():
    return {"events": events[-50:]}
