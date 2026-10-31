# Multi-device LAN sandbox

A small, safe prototype of the multi-device workspace: one coordinator plus three independently running device nodes, all on a private Docker Compose bridge network.

## Important distinction

These are **Linux containers**, not full virtual machines. GitHub Codespaces supplies the cloud-hosted development machine; Docker Compose runs several isolated services inside it. The services can address one another by name on their private network. This gives us a reproducible intranet-like test bed without paying for or managing several separate VMs.

GitHub stores the configuration and source code. It does not keep these services running after the Codespace is stopped. This sandbox does not connect to your home devices or expose the node ports publicly.

## Emulated layout

- `coordinator`: central registry and event receiver, exposed on port 8788 through the Codespace.
- `device-browser`: represents a browser/workstation node.
- `device-model`: represents a local-model/compute node.
- `device-audio`: represents an audio/DAW node.

All three nodes send periodic heartbeats to the coordinator over the private Compose network. Only the coordinator publishes a port.

## Start it

From the repository root, in a GitHub Codespace terminal:

```bash
cd labs/multidevice-lan
docker compose up --build -d
docker compose ps
```

Then open port **8788** from the Codespaces Ports panel. The status page is at `/`, health at `/health`, and the live node registry at `/nodes`.

To inspect logs:

```bash
docker compose logs -f
```

To stop the sandbox:

```bash
docker compose down
```

## Network model

Compose creates a private bridge network named `sophia-lan`. Containers resolve one another by service name. The worker nodes have no published host ports; they call `http://coordinator:8788` internally. The coordinator's one published port is the deliberate observation window into the sandbox.

This is a prototype of the network topology, not yet a recreation of the historical computers, their actual applications, credentials, models, audio devices, or cloud services. We should map those from recovered artifacts before adding them.

## Safety and cost

No secrets, API keys, personal files, or host folders are mounted into the nodes. No privileged containers or host networking are used. The services are lightweight and do not download or run language models. Codespaces usage may incur charges according to the account's plan and included quota; stop or delete the Codespace when finished.
