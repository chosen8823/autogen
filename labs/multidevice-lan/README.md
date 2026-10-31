# Multi-device LAN sandbox

A reproducible cloud-hosted prototype of the historical multi-device workspace. One coordinator, three device-role nodes, and a shared XYZ-grid/codex service run as separate containers on a private Docker Compose network.

## What this is

These are Linux containers, **not four full virtual machines**. A GitHub Codespace supplies one cloud development machine; Docker Compose runs multiple isolated services inside it. The services resolve one another by name on their private bridge network. This proves the network topology before we spend money on separate VMs.

GitHub stores the source and configuration; it does not keep the services running after the Codespace stops. This prototype does not connect to home devices, expose worker ports, or load personal API keys.

## Services

- `coordinator` — device registry and event receiver, port 8788.
- `device-browser` — emulates a browser/workstation role.
- `device-model` — emulates a local-model/compute role.
- `device-audio` — emulates an audio/DAW role.
- `codex-grid` — shared project-semantic XYZ grid and codex API, port 8791.

The three device nodes send heartbeats to the coordinator every five seconds. Only the coordinator and grid API publish ports; worker nodes remain private.

## Launch

Open this repository in GitHub Codespaces using branch `feat/multidevice-lan-sandbox`. In the terminal:

```bash
cd labs/multidevice-lan
docker compose up --build -d
docker compose ps
```

Open forwarded port 8788 for the device network and port 8791 for the grid/codex API. The devcontainer config requests automatic forwarding for both.

Useful endpoints:

- Coordinator: `/`, `/health`, `/nodes`, `/events`
- Grid/codex: `/health`, `/grid`, `/grid/activate`, `/codex`

Interactive API documentation is available at `/docs` on each service.

To stop: `docker compose down`. To inspect: `docker compose logs -f`.

## XYZ grid and codex

The grid service initializes 9 × 6 × 3 = 162 addressable nodes. It exposes a small REST interface for reading the grid, activating a coordinate, and recording a source label. The codex endpoint stores named entries with title, body, semantic plane, source, and tags.

The service preserves our project's own coordinate model as software semantics. It does not imply that the grid is a physical field or that its frequency values produce medical, neurological, or supernatural effects. The initial service is in-memory: entries reset when its container is recreated. Persistent storage and migration of the original codex are a later step, after we identify the canonical source files and agree on their provenance.

## Network and safety

Compose creates a private bridge network named `sophia-lan`. Containers resolve each other by service name. Worker nodes have no published host ports. No secrets, personal files, host folders, privileged mode, or host networking are used. No language models are downloaded or run.

Codespaces usage can incur charges. Personal GitHub accounts have a monthly included compute/storage quota; check current usage and budgets before starting. Stop or delete the Codespace when finished.
