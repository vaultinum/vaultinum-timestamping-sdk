# Vaultinum Timestamping Python SDK

This module is a simple client for the Vaultinum's Timestamping service.

## Usage

From the command line:

```bash
# Install requirements
pip install -r requirements.txt
# Run the module
python -m vaultinumts --help
```

From python:

```python
>>> import vaultinumts
>>> vaultinumts.timestamp("data.txt", "sandbox", "YOUR_SANDBOX_APIKEY")
```
