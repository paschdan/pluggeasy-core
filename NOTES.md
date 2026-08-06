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
| `pluggeasy-modbus` library | `0.2.0` | Pinned in `manifest.json` `requirements`. |
| This integration | — | No standalone version; follows HA core release cycle. |
| `pluggeasy-hacs` | `0.2.0` | Parallel HACS deliverable for standalone installs. |

## Architecture note

This integration uses the **shared-connection** model: the user configures a `modbus_connection` entry once in HA, and this integration's config flow uses `ConfigEntrySelector` to reference it. The `modbus_connection` HA component is listed in `manifest.json` `dependencies`.

For a self-contained installation that owns its own Modbus TCP connection, see [`pluggeasy-hacs`](https://github.com/paschdan/pluggeasy-hacs).

## What changed in 0.2.0

- **`fan.py`** (new) — `PluggeasyFan` entity with preset modes `low`, `medium`, `nominal`, `auto`, `snooze`. `turn_on` defaults to `nominal`; `turn_off` sets `snooze`. Writes `selected_airflow` holding register via `async_set_airflow()`.
- **`button.py`** (new) — `PluggeasyButton` entity (category: config) for filter alarm reset. Calls `async_reset_filter_alarm()`.
- **`sensor.py`** — `actual_working_mode`, `defrost_status`, `communication_error`, `bypass_damper_position` converted to `SensorDeviceClass.ENUM` sensors with human-readable state names. `selected_airflow` sensor removed (now fan entity). Total: 24 sensors (was 25).
- **`switch.py`** — `working_mode` coil switch and `reset_filter_alarm` switch removed. Total: 5 switches (was 7).
- **`binary_sensor.py`** — `boost_mode_active` renamed to `boost_active`; reads the corrected `status.boost_active` property (inverted).
- **`__init__.py`** — `Platform.FAN` and `Platform.BUTTON` added.
- **`strings.json`** — fan/button names and enum state translations added.
