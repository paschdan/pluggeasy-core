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
| `sensor` | 24 | Air temperatures, humidity, motor voltages/RPM, VOC, enum status sensors (actual working mode, defrost status, communication error, bypass damper position), parameters |
| `switch` | 5 | Bypass, summer mode, boost, snooze, allow automatic bypass |
| `fan` | 1 | Ventilation speed (presets: low / medium / nominal / auto / snooze) |
| `button` | 1 | Reset filter alarm |

## Requirements

- Home Assistant ≥ 2026.6.4
- `modbus_connection` HA component (shared connection)
- `pluggeasy-modbus==0.3.0` (PyPI, installed automatically via `requirements`)

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
├── sensor.py            # 24 EntityDescriptions (4 enum sensors)
├── switch.py            # 5 EntityDescriptions
├── fan.py               # 1 FanEntity (speed presets)
├── button.py            # 1 ButtonEntity (reset filter alarm)
├── strings.json         # UI strings
└── quality_scale.yaml   # Bronze quality scale
```

## Device library

The Modbus data model is provided by [`pluggeasy-modbus`](https://github.com/paschdan/pluggeasy-modbus) (`pluggeasy-modbus==0.3.0`). That library is transport-agnostic and takes a `ModbusUnit` from `modbus_connection`.

## HACS / standalone installation

For a self-contained installation that does not require the `modbus_connection` HA component, see [`pluggeasy-hacs`](https://github.com/paschdan/pluggeasy-hacs).

## Breaking changes in 0.2.0

> **Users upgrading from 0.1.0 must update any automations referencing the old entity IDs.**

| Change | Old entity_id suffix | New entity_id suffix / replacement |
| :--- | :--- | :--- |
| Boost binary sensor renamed + inverted | `boost_mode_active` | `boost_active` (value now correct: `on` = boost running) |
| Speed control replaced by fan entity | `selected_airflow` sensor | `fan.pluggeasy` (preset modes) |
| Working mode switch removed | `working_mode` switch | Folded into fan entity (Auto preset) |
| Filter reset switch replaced by button | `reset_filter_alarm` switch | `button.pluggeasy_reset_filter_alarm` |

**Unchanged switches**: `manual_bypass`, `allow_automatic_bypass`, `summer_mode`, `manual_boost`, `snooze_mode`.
