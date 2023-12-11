# Vaultinum Timestamping Python SDK

This module is a simple client for the Vaultinum's Timestamping service.

## Installation

This package is available on PyPI :

```bash
python -m pip install vaultinum-ts
```

## Usage

```bash
python -m vaultinum_ts --help
python -m vaultinum_ts -filename data.txt -environment sandbox -apikey YOUR_SANDBOX_APIKEY
```

```python
>>> from vaultinum_ts import timestamp
>>> timestamp("data.txt", "sandbox", "YOUR_SANDBOX_APIKEY")
```
