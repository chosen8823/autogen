"""Shared semantic XYZ grid service for the multi-device sandbox.

This is a software model of the project's locally defined 9x6x3 grid.
It does not claim physical or neurological effects.
"""
import math
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Sophia Codex and XYZ Grid", version="0.1.0")
grid: dict[str, dict[str, Any]] = {}
events: list[dict[str, Any]] = []


def key(x: int, y: int, z: int) -> str:
    if not (0 <= x < 9 and 0 <= y < 6 and 0 <= z < 3):
        raise HTTPException(status_code=422, detail="Coordinates must satisfy X 0..8, Y 0..5, Z 0..2")
    return f"{x},{y},{z}"


for x in range(9):
    for y in range(6):
        for z in range(3):
            grid[key(x, y, z)] = {
                "x": x, "y": y, "z": z,
                "activation": 0.0,
                "resonance_hz": 432.0,
                "labels": [],
                "updated_at": time.time(),
            }


class Activation(BaseModel):
    x: int = Field(ge=0, le=8)
    y: int = Field(ge=0, le=5)
    z: int = Field(ge=0, le=2)
    amount: float = Field(default=1.0, ge=0.0, le=1.0)
    label: str | None = None
    source: str = "unknown"


class CodexEntry(BaseModel):
    entry_id: str
    title: str
    body: str
    plane: str = "semantic"
    source: str = "user-authored"
    tags: list[str] = []


codex: dict[str, dict[str, Any]] = {}


@app.get("/health")
def health():
    return {"ok": True, "service": "codex-grid", "nodes": len(grid)}


@app.get("/grid")
def read_grid():
    return {"dimensions": [9, 6, 3], "count": len(grid), "nodes": list(grid.values())}


@app.post("/grid/activate")
def activate(message: Activation):
    item = grid[key(message.x, message.y, message.z)]
    item["activation"] = min(1.0, item["activation"] + message.amount)
    item["updated_at"] = time.time()
    if message.label and message.label not in item["labels"]:
        item["labels"].append(message.label)
    event = {
        "source": message.source,
        "coordinate": [message.x, message.y, message.z],
        "amount": message.amount,
        "time": time.time(),
    }
    events.append(event)
    del events[:-200]
    return {"node": item, "event": event}


@app.get("/events")
def read_events():
    return {"events": events[-100:]}


@app.put("/codex/{entry_id}")
def put_codex(entry_id: str, entry: CodexEntry):
    if entry_id != entry.entry_id:
        raise HTTPException(status_code=400, detail="Path ID must match entry_id")
    codex[entry_id] = entry.model_dump()
    return {"saved": True, "entry": codex[entry_id]}


@app.get("/codex")
def read_codex():
    return {"count": len(codex), "entries": list(codex.values())}
