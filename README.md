# `pluggeasy-core` — Home Assistant Core Integration

[![CI](https://github.com/paschdan/pluggeasy-core/actions/workflows/ci.yml/badge.svg)](https://github.com/paschdan/pluggeasy-core/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/paschdan/pluggeasy-core.svg)](LICENSE)

Home Assistant **core integration** for the Pluggeasy (Pluggit) heat-recovery ventilation unit.

## What is this?

This repository contains the `pluggeasy` integration intended for inclusion in the [Home Assistant core](https://github.com/home-assistant/core) repository. It lives under `homeassistant/components/pluggeasy/` and follows the HA core integration layout and quality standards.

It uses the **shared `modbus_connection` component** (`async_get_unit`) so it does not own the Modbus transport — the user configures the connection once in HA and selects it in the integration's config flow.

## Entities provided

| Platform | Count | Description |
| :--- | :---: | :--- |
| `binary_sensor` | 11 | Alarms, sensor faults, fan faults, bypass/boost status |
| `sensor` | 25 | Air temperatures, humidity, motor voltages/RPM, VOC, working mode, parameters |
| `switch` | 7 | Filter reset, bypass, summer mode, boost, snooze, working mode |

## Requirements

- Home Assistant ≥ 2026.6.4
- `modbus_connection` HA component (shared connection)
- `pluggeasy-modbus==0.1.0` (PyPI, installed automatically via `requirements`)

## Integration layout

```
homeassistant/components/pluggeasy/
├── manifest.json        # domain, requirements, dependencies
├── const.py             # DOMAIN, CONF_* constants
├── coordinator.py       # DataUpdateCoordinator wrapping the device library
├── entity.py            # PluggeasyEntity base (CoordinatorEntity)
├── config_flow.py       # ConfigEntrySelector (shared connection) + unit id
├── __init__.py          # async_setup_entry / async_unload_entry
├── binary_sensor.py     # 11 EntityDescriptions
├── sensor.py            # 25 EntityDescriptions
├── switch.py            # 7 EntityDescriptions
├── strings.json         # UI strings
└── quality_scale.yaml   # Bronze quality scale
```

## Device library

The Modbus data model is provided by [`pluggeasy-modbus`](https://github.com/paschdan/pluggeasy-modbus) (`pluggeasy-modbus==0.1.0`). That library is transport-agnostic and takes a `ModbusUnit` from `modbus_connection`.

## HACS / standalone installation

For a self-contained installation that does not require the `modbus_connection` HA component, see [`pluggeasy-hacs`](https://github.com/paschdan/pluggeasy-hacs).
