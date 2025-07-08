# Spedion Truck Import

This tool automates the import of newly registered trucks into the SPEDION telematics system using their SOAP API.

## Features

- Connects to MS SQL Server (WinSped)
- Selects newly registered trucks
- Sends structured XML payload to SPEDION SOAP service
- Avoids duplicates using a local log file
- Supports German and English environment

## Configuration

1. Set your DB credentials and SOAP authentication via environment variables or secure config.
2. Create or provide `LIST_PATCH.txt` to track processed vehicles.

## Run

```bash
python main.py
```

## License

MIT License
