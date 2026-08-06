# NOTES — pluggeasy-core

## Cross-repo links

| Repo | Purpose |
| :--- | :--- |
| **[pluggeasy-modbus](https://github.com/paschdan/pluggeasy-modbus)** | Transport-agnostic Python device library |
| **[pluggeasy-core](https://github.com/paschdan/pluggeasy-core)** (this repo) | HA core integration (shared `modbus_connection` component) |
| **[pluggeasy-hacs](https://github.com/paschdan/pluggeasy-hacs)** | HACS custom integration (own-connection, self-contained) |

## Versions

| Artifact | Version | Notes |
| :--- | :--- | :--- |
| `pluggeasy-modbus` library | `0.1.0` | Pinned in `manifest.json` `requirements`. |
| This integration | — | No standalone version; follows HA core release cycle. |
| `pluggeasy-hacs` | `0.1.0` | Parallel HACS deliverable for standalone installs. |

## Architecture note

This integration uses the **shared-connection** model: the user configures a `modbus_connection` entry once in HA, and this integration's config flow uses `ConfigEntrySelector` to reference it. The `modbus_connection` HA component is listed in `manifest.json` `dependencies`.

For a self-contained installation that owns its own Modbus TCP connection, see [`pluggeasy-hacs`](https://github.com/paschdan/pluggeasy-hacs).
