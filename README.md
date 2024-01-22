**Read this in other languages: [English](README.md), [中文](README_zh.md).**


# qBittorrent Client Xunlei

This script automates the process of filtering unwanted clients from qBittorrent based on predefined rules.

## Features

- Automatically logs into qBittorrent Web UI.
- Retrieves the list of downloading/uploading torrents.
- Queries the connected clients for each torrent.
- Applies user-defined rules to filter out unwanted clients.
- Updates the IP filter of qBittorrent to block the filtered clients.
- Periodically checks the status and performs the above steps.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (install via `pip install -r requirements.txt`):
  - `requests`
  - `json`
  - `time`
  - `random`
  - `math`
  - `string`
  - `configparser`
  - `os`

### Configuration

1. Rename `config_sample.ini` to `config.ini`.
2. Open `config.ini` and configure the following settings:
   - **Credentials:** Set your qBittorrent Web UI username and password.
   - **URLs:** Set the root URL of your qBittorrent Web UI.
   - **Paths:** Set the file path for the IP filter.

### Filter Rules

Modify the `[FilterRules]` section in `config.ini` to define your custom filter rules. Each rule should follow the format `name,findType` where `findType` is `1` for contains matching and `2` for prefix matching.

Example:
```ini
[FilterRules]
# Filter rules for blocking clients
# Each rule is defined with the format: name,findType
# where findType is 1 for contains matching, 2 for prefix matching
rule_1 = -XL0012,1
rule_2 = -XL0012-,1
rule_3 = Xunlei,1
rule_4 = Xfplay,1
rule_5 = go.torrent,1
rule_6 = QQDownload,1
rule_7 = 7.,2
```


# Usage

```ini
python qBittorrentBan.py
```

The script will continuously run, periodically checking and updating the IP filter in qBittorrent.

